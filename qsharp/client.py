import subprocess
import time
import http.client
import atexit
import json
import sys
import urllib.parse
import os

from collections import defaultdict
from typing import List, Dict
from qsharp.version import __version__

## EXPORTS ##
# There's a lot of internals like qssProc that we want to hide, so we explicitly
# list what gets imported by default.

__all__ = [
    'get_available_operations',
    'get_available_operations_by_namespace',
    'simulate',
    'trace'
]

## LOGGING ##

import logging
logger = logging.getLogger(__name__)

## MODULE-LEVEL GLOBALS ##

qssProc = None

## CONSTANTS ##

QSS_PATH = os.path.dirname(__file__)
QSS_EXE  = os.path.join(QSS_PATH, "qss")

logger.debug(f"""
    Q# server path:       {QSS_PATH}
    Q# server executable: {QSS_EXE}
""")

## FUNCTIONS ##

def printMessages(data):
    msgs = data['messages']
    for msg in msgs:
        print(msg)

def processErrors(data):
    print("\n---------------------------------------------------")
    print("Q# errors:")
    printMessages(data)
    print("---------------------------------------------------\n")
    raise Exception("Failed to call Q#")

def buildUrl(op, action, params):
    # Tuples are json encoded differently in C#, this makes sure they are in the right format.
    def map_tuples(obj):
        if isinstance(obj, tuple):
            result = {}
            for i in range(len(obj)):
                result[f"item{i+1}"] = map_tuples(obj[i])
            return result
        if isinstance(obj, list):
            result = []
            for i in obj:
                result.append(map_tuples(i))
            return result
        else:
            return obj
    args = {}
    for key, value in params.items():
        args[key] = map_tuples(value)
    query = urllib.parse.urlencode(args)
    url =  f'/api/operations/{op}/{action}?{query}'
    #print("url: ", url)
    return url



def callQsS(url):
    conn = http.client.HTTPConnection("localhost", 5050)
    conn.request("GET", url)
    return conn.getresponse()


def processResponse(r):
    def unmap_tuples(obj):
        if 'item1' in obj:
            result = tuple(obj.values())
            return result
        else:
            return obj
    data = json.loads(r.read(), object_hook=unmap_tuples)
    #print("response: ", data)
    if data['status'] != 'success':
        processErrors(data)
    else:
        printMessages(data)
    return data

def get_available_operations() -> List[str]:
    """
    """
    response = callQsS("/api/operations")
    data = processResponse(response)
    return data['result']

def get_available_operations_by_namespace() -> Dict[str, str]:
    ops = get_available_operations()
    by_ns = defaultdict(list)

    for qualified_name in ops:
        idx_last_dot = qualified_name.rfind(".")
        ns_name = qualified_name[:idx_last_dot]
        op_name = qualified_name[idx_last_dot + 1:]

        by_ns[ns_name].append(op_name)

    return dict(by_ns.items())

def simulate(op, **params):
    url =  buildUrl(op, "simulate", params)
    response = callQsS(url)
    data = processResponse(response)
    return data['result']

def trace(op, **params):
    url =  buildUrl(op, "trace", params)
    response = callQsS(url)
    data = processResponse(response)
    return data['result']

def installQss():
    try:
        print("Importing qsharp for the first time. Installing backend.")
        subprocess.run([
            "dotnet", "tool", "install",
            "--add-source", os.path.dirname(__file__),
            "--tool-path", QSS_PATH,
            "--version", __version__,
            "qss"
        ])
    except:
        data = {}
        data['messages'] = [
            "The qsharp module depends on .NET Core SDK 2.1.300 or later.",
            "Please take a moment to install .NET Core from: https://dotnet.microsoft.com/download"
        ]
        processErrors(data)

def checkQssInstalled():
    ready = False
    try:
        result = subprocess.run([QSS_EXE, "--version"], stdout=subprocess.DEVNULL)
        ready = (result.returncode == 0)
    except Exception:
        ready = False
    if not ready:
        installQss()

# Make sure the process is stopped when Python exists:
def stopProc():
    global qssProc
    #print ("Stopping Q# process")
    if not qssProc is None: 
        qssProc.terminate()



# When the module is imported, start the Q# server (unless --skipQSS is specified in the command line):
if not ('--skipQSS' in sys.argv):
    checkQssInstalled()
    qssProc = subprocess.Popen(QSS_EXE, stdout=subprocess.DEVNULL)
atexit.register(stopProc)


# Check if the server is up and running:
qssReady = False
for i in range(1,10):
    try:
        r = callQsS("/api/operations")
        qssReady = r.status == 200
        if qssReady:
            break
    except:
        if i == 1:
            print("Preparing Q# environment...")
        time.sleep(1)

if not qssReady:
    raise Exception("Q# environment was not available in allocated time.")


