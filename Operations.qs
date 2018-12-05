///
/// Q# code should be in one or more .qs files that live 
/// in the same directory as the python clasical driver.
///
namespace Microsoft.Prototypes.Python
{
    open Microsoft.Quantum.Primitive;

    /// # Summary: 
    ///     The simplest program. Just generate a debug Message on the console.
    operation HelloQ() : Unit
    {
        Message($"Hello from quantum world!"); 
    }

    /// # Summary: 
    ///     A more sophisticated program that shows how to 
    ///     specify parameters, instantiate qubits, and return values.
    operation HelloAgain(count: Int, name: String) : Result[]
    {
        Message($"Hello {name} again!"); 

        mutable r = new Result[count];
        using (q = Qubit()) {
            for (i in 1..count) {
                H(q);
                set r[i-1] = M(q);
                Reset(q);
            }
        }

        return r;
    }
}
