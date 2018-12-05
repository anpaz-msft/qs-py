# Legal

This is pre-release software provided under NDA, please treat it accordingly.


# Pre-requisites.

The Q# compiler and simulation framework requires .NET core 2.1.300 or later.
Please take a moment to install .NET Core from: https://dotnet.microsoft.com/download

This prototype requires Python 3.6. It has been tested with Python 3.6.5. 

For the best experience developing Q# it is recommended, but not required, to install the rest of the
Microsoft Quantum Developement Kit. Instructions for VS Code are found [here](https://docs.microsoft.com/en-us/quantum/install-guide/command-line?view=qsharp-preview).


# Python Package Installation

For this prototype version, download the qsharp Python package from:
https://aka.ms/qsharp-py-prototype

Then extract the contents of the zip file into the root folder of your project, where
your Python and Q# code will live. Once extrated, you should see a `qsharp` directory in your 
root directory. For example:

```
  + Project
    - driver.py
    - Operations.qs
    + qsharp
```

# Usage

Create one or more files with a `.qs` extension with the quantum operations you want to execute.
The qsharp module automatically detects and tries to compile all the files under the current 
diretory that have the  `.qs` extension.

To call a Q# operation from Python, first import the `qsharp` module:
```python
import qsharp
```

After this, Q# namespaces can be imported as Python packages, for example:
```python
from Microsoft.Prototypes.Python import HelloQ, HelloAgain
```

Once imported, to simulate a Q# operation invoke it's `simulate` method:
```python
HelloQ.simulate()
```

If the Q# operation expects parameters, include them as named parameters to the `simulate` method:
```python
HelloAgain.simulate(count=3, name="Brilliant")
```

If the Q# operation returns a value, the corresponding value is returned from the `simulate` method.
```python
r = HelloAgain.simulate(count=3, name="Brilliant")
print("HelloAgain result: ", r)
```

On top of simulation, you can also do quantum resources estimation including 
the count of primitive operations used by the algorithm and the number of required qubits.
For this, invoke the `trace` method on the operation:
```python
r = HelloAgain.trace(count=5, name="Counting")
```

You may use the `qsharp.printTracerCounts` method to print the trace results to the console:
```python
qsharp.printTracerCounts(r)
```


# Performance optimizations

Behind the scenes, when loaded, the `qsharp` module starts a `qss` server that gets terminated
when Python finishes execution. To improve performance and avoid the server's initialization costs 
the `qss` server can be externally started and kept alive.

## Installing `qss`

Once the `qsharp` package has been installed in your project, from the project's root folder execute:
```
python -c "import qsharp"
```

## Running `qss`

Once installed, to start the `qss` server, from a command line in your projects' root folder execute:
```
qsharp\qss
```

> The server must be started from the project's root folder to 
> discover the `.qs` files

If started successfully, you will see the following message:
```
Now listening on: http://localhost:5050
Application started. Press Ctrl+C to shut down.
```

## Invoking QSS:

From another command line, you can now execute your Python driver passing the `--skipQss` parameter,
for example:
```
python driver.py --skipQss
```

You may do any changes to your `.qs` files while the qss server is running, the changes are 
automatically picked up the next time you try to invoke the quantum operations from Python.



