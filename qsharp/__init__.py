from qsharp.client import *

import qsharp.loader
from qsharp.version import __version__

def printTracerCounts(data):
    counts = data['counts']
    for key, value in counts.items():
        print(key, ":")
        print(value)
        print()