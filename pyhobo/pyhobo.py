try:
    from openfermion.ops import QubitOperator
    import numpy as np
except (ModuleNotFoundError, ImportError):
    raise ImportError("OpenFermion is not installed or cannot be imported. Please make sure OpenFermion is installed.")

# need linear algebra and spin operator packages
from openfermion.ops import QubitOperator
import numpy as np

# Continue with the rest of your code that depends on OpenFermion

class Binary: 

    """
    Constructs operator representation of binary variables using hobo encoding.

	The `binary` class wraps most of the functionalty of the PyHOBO package. This object allows the user to construct 
    operator associated with binary variable in hobo encoding, and further used to construct hamiltonian.

	Notes
	-----
	One can instantiate the class by parsing number of nodes and position where the counting begin with 0 (parthavi).

	"""

    def __init__(self, num_nodes, num_positions):

        """
        Initialize the Binary class with num_nodes and num_positions.
        
        Parameters:
        num_nodes (int): The upper limit for node, must be > 0.
        num_positions (int): The upper limit for pos, must be > 0.
        """
        # Validate inputs
        if num_nodes <= 0:
            raise ValueError(f"num_nodes must be > 0, but got {num_nodes}.")
        if num_positions <= 0:
            raise ValueError(f"num_positions must be > 0, but got {num_positions}.")

        # Assign to instance variables
        self.num_nodes = num_nodes
        self.num_positions = num_positions

        # Calculate number of qubits
        self.num_qubits = num_positions * int(np.ceil(np.log2(num_nodes)))
        self.node_qubits = int(np.ceil(np.log2(num_nodes)))

    def __repr__(self):
        return f"Binary(num_nodes={self.num_nodes}, num_positions={self.num_positions})"

    def op_str(self, node, pos):
        if not (0 <= node < self.num_nodes):
            raise ValueError(f"node must be >= 0 and < {self.num_nodes}, but got {node}.")
        if not (0 <= pos < self.num_positions):
            raise ValueError(f"pos must be >= 0 and < {self.num_positions}, but got {pos}.")

        op = self._compute_op(node, pos)
        op_terms = op.terms
        op_str = []

        for key, value in op_terms.items():
            str_list = ['I' for _ in range(self.num_qubits)]  
            for item in key:
                str_list[item[0]] = 'Z'
            op_str.append((''.join(str_list), value))

        return op_str

    def _compute_op(self, node, pos):
        Ait = QubitOperator('')
        bin_arr = self._num2bin(node, self.node_qubits)
        for i in range(self.node_qubits):
            if bin_arr[i] == 1:
                Ait = Ait * self._proj_on_1(i + pos * self.node_qubits)
            else:
                Ait = Ait * self._proj_on_0(i + pos * self.node_qubits)

        return Ait

    @staticmethod
    def _proj_on_0(i):
        identity_op = QubitOperator('')
        pauli_z = QubitOperator('Z' + str(i))
        return 0.5 * (identity_op + pauli_z)

    @staticmethod
    def _proj_on_1(i):
        identity_op = QubitOperator('')
        pauli_z = QubitOperator('Z' + str(i))
        return 0.5 * (identity_op - pauli_z)

    @staticmethod
    def _num2bin(number, length):
        bin_str = bin(number)[2:]  # Get binary representation as a string, removing the '0b' prefix
        pad_bin_str = bin_str.zfill(length)  # Pad with leading zeros to ensure fixed length
        bin_arr = np.array([int(bit) for bit in pad_bin_str])  # Convert binary string to numpy array
        return bin_arr



class Hamiltonian:
    """
	The `Hamiltonian` class wraps most of the functionalty of the PyHOBO package. This object allows the user to construct 
    operator associated with binary variable in hobo encoding, and further used to construct hamiltonian.

	Notes
	-----
	One can instantiate the class by parsing number of nodes and position where the counting begin with 0 (parthavi).
	"""
    def __init__(self, binary: Binary, terms: list):
        """
        Initialize the Hamiltonian class with a Binary object and a list of terms.
        
        Parameters:
        binary (Binary): An instance of the Binary class.
        terms (list): A list of terms, where each term is a list containing a coefficient and a list of [node, pos] pairs.
                        Example: [[coeff1, [[node1, pos1], [node2, pos2], ...]], [coeff2, ...]]
        """

        if not isinstance(terms, list):
            raise TypeError("Input 'terms' must be a list.")

        for term in terms:
            if not isinstance(term, list) or len(term) != 2:
                raise ValueError("Each term in 'terms' must be a list of length 2.")

            coeff, node_pos_pairs = term
            if not isinstance(coeff, (int, float, complex)):
                raise ValueError("Coefficient in each term must be a numeric value.")

            if not isinstance(node_pos_pairs, list):
                raise ValueError("Node and position pairs in each term must be provided as a list.")

            for node_pos_pair in node_pos_pairs:
                if not isinstance(node_pos_pair, list) or len(node_pos_pair) != 2:
                    raise ValueError("Each node and position pair must be a list of length 2.")

                node, pos = node_pos_pair
                if not (isinstance(node, int) and isinstance(pos, int)):
                    raise ValueError("Node and position values must be integers.")


        self.binary = binary
        self.terms = terms

    def __repr__(self):
        return f"Hamiltonian(terms={self.terms})"

    def ham_op(self):
        hamiltonian = QubitOperator('')
        for term in self.terms:
            coeff = term[0]
            node_pos_pairs = term[1]
            term_op = QubitOperator('')
            for node, pos in node_pos_pairs:
                term_op *= self.binary._compute_op(node, pos)
            hamiltonian += coeff * term_op
        return hamiltonian

    def ham_op_str(self, offset = True):
        ham_str = []
        hamiltonian = self.ham_op()
        op_terms = hamiltonian.terms

        for key, value in op_terms.items():
            str_list = ['I' for _ in range(self.binary.num_qubits)]  
            for item in key:
                str_list[item[0]] = 'Z'
            ham_str.append((''.join(str_list), value))

        # if offset is true, then remove the identity.
        if offset:
            ham_str.pop(0)
            
        return ham_str

