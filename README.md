# PyHOBO

If you want to solve a combinatorial optimization problem using Higher-Order Binary Optimization, PyHOBO allows you to construct cost function or Hamiltonian for your problem which can directly be fed to Qiskit. PyHOBO is based on functonalities of OpenFermion such as in solving for Pauli strings.

PyHOBO is at its initial stage with number of functionalities still to be addressed.

## Install it from PyPI

```bash
pip install pyhobo
```

## Usage

The example shown below construct a operator associated with binary variable $b_{it}$ defined in [npj Quantum Inf 8, 39 (2022)](https://doi.org/10.1038/s41534-022-00546-y).

```py
from pyhobo import Binary
b = Binary(num_nodes=5, num_positions=4)
print(b)
print(b._compute_op(node=2, pos=3))
```

<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.
