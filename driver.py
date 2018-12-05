# To start, simply import the qsharp module.
import qsharp

# After importing the qsharp module, Q# namespaces can be imported like any
# other Python packages.
from Microsoft.Prototypes.Python import HelloQ, HelloAgain

# All Q# operations defined in any .qs file inside the same working directory
# is automatically identified.
# You can simulate any of them simply by calling the `simulate` method
# on Q# functions and operations once they've been imported.
r = HelloQ.simulate()
print("HelloQ result: ", r)
print("")

# If the operation receives parameters, just include them as named parameters
# of the same simulate method.
r = HelloAgain.simulate(count=3, name="Brilliant")
print("HelloAgain result: ", r)
print("")


# On top of simulation, you can also do quantum resources estimation including 
# the count of primitive operations used by the algorithm and the number of required qubits.
# For this, invoke the `trace` method on the operation:
r = HelloAgain.trace(count=5, name="Counting")

# You may use the `printTracerCounts` function `qsharp` to print the results to the console:
qsharp.printTracerCounts(r)
