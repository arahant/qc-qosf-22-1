import sys
import algorithm
from models import Board, Quantum

def parse_initial_state(given_state):
    empty = set()
    state = set()
    bot = set()
    size = 0
    # TODO: replace this with actual qubits
    for i, s in enumerate(given_state):
        size += 1
        if s == '1':
            state.add(i+1)
        elif s == '0':
            bot.add(i+1)
        else:
            empty.add(i+1)
    return state, bot, empty, size

def get_resulting_qubit(qubit, empty, state):
    res = ''
    bot = empty - state
    for i, q in enumerate(qubit):
        if i+1 in state:
            res += '1'
        elif i+1 in bot:
            res += '0'
        else:
            res += '.'
    return res

if __name__ == '__main__':
    initial_state, bot, empty, size = parse_initial_state(sys.argv[1])
    max_moves = int(sys.argv[2])
    # Setting the initial state of qubits based on the given circuit
    quantum = Quantum(initial_state, bot, size)
    board = Board(initial_state, bot, size, empty, max_moves)
    your_turn = (board.size - board.empty)%2 != 0
    total_set = set(range(size+1))

    print("\nGiven Inputs:")
    print(" Initial qubit state:", '|'+sys.argv[1].replace('x', '.')+'⟩')
    print(" Player's initial positions:", initial_state)
    print(" Bot's initial positions:", bot)
    print(" Empty cells at: ", empty)
    # print(" Quantum Circuit: ")
    # print(quantum.circuit)

    algorithm.make_move(quantum, board, your_turn, 1, list(initial_state), 0, 0, [])
    best_wins, win_moves, win_circuits = algorithm.get_result(board)

    print("\nFinal Qubits", "\t Resultant Qubit", "  Probability", "\t Steps", "\t Player's moves")
    for probability in sorted(best_wins.keys(), reverse=True):
        for steps, state in best_wins[probability]:
            qubit = algorithm.get_qubit(state, total_set-set(state), size)
            result = get_resulting_qubit(qubit, empty, set(state)-initial_state)
            print('|'+qubit+'⟩', '\t', '|'+result+'⟩', '\t  ', probability, '\t', steps, '\t', list(win_moves[state]))

    for state in win_circuits.keys():
        circuit = win_circuits[state]
        qubit = algorithm.get_qubit(state, total_set-set(state), size)
        print("\nResultant Quantum Circuits for: ", '|'+qubit+'⟩')
        print(circuit)
