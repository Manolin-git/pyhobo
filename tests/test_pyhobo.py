from pyhobo import Binary, Hamiltonian

# Example usage 1
try:
    b = Binary(num_nodes=5, num_positions=4)
    print(b)
    print(b._compute_op(node=2, pos=3))
except ValueError as e:
    print(e)

# Example usage 2
try:
    binary = Binary(num_nodes=5, num_positions=4)
    terms = [
        [1.5, [[2, 3], [1, 2]]],
        [-2.0, [[0, 1]]]
    ]
    hamiltonian = Hamiltonian(binary, terms)
    print(hamiltonian)
    print(hamiltonian.ham_op())
    print(hamiltonian.ham_op_str())
except ValueError as e:
    print(e)