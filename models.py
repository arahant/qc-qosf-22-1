import qiskit as qk

LOGGING = False

INITIAL_STATE_PLAYER = [0,1]     # Define initial_state as |1⟩
INITIAL_STATE_BOT = [1,0]     # Define initial_state as |0⟩
INITIAL_STATE_REST = [1,0]  # Define initial_state as |0⟩

class Quantum():

    def __init__(self, state, bot, size):
        self.size = size
        self.qubits = qk.QuantumRegister(size)
        self.bits = qk.ClassicalRegister(size)
        self.circuit = qk.QuantumCircuit(self.qubits, self.bits)
        self.initialize_qubits(state, bot)

    def initialize_qubits(self, state, bot):
        """
        Given the initial state of the board, the qubits are initialized as follows:
        1. Player's qubits are set to |1⟩
        2. Bot's qubits are set to |0⟩
        3. Borrowed are set to |0⟩
        """
        for i in range(self.size):
            if i+1 in state:
                self.circuit.initialize(INITIAL_STATE_PLAYER, i)
            elif i in bot:
                self.circuit.initialize(INITIAL_STATE_BOT, i)
            else:
                self.circuit.initialize(INITIAL_STATE_REST, i)


class Board():

    def __init__(self, state, bot, size, empty, max):
        """
        Board.state: represents the current state of the game board
        Board.empty_cells = list of empty cells left to play for
        Board.moves: # moves left for the player
        """
        self.state = state
        self.bot = bot
        self.size = size
        self.available = empty
        self.empty = len(empty)
        self.max = max


class Result():

    def __init__(self, best_wins, win_moves, win_circuits):
        self.best_wins = best_wins
        self.win_moves = win_moves
        self.win_circuits = win_circuits
