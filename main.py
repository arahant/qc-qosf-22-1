import sys
from itertools import permutations
import algorithm
from models import Board, Quantum

def parse_initial_state(given_state):
    empty = set()
    state = set()
    bot = set()
    size = 0
    for i, s in enumerate(given_state):
        size += 1
        if s == '1':
            state.add(i+1)
        elif s == '0':
            bot.add(i+1)
        else:
            empty.add(i+1)
    return state, bot, empty, size


def initial_log(initial_state, bot, empty):
    print("\nGiven Inputs:")
    print("  Initial qubit state:", '|'+sys.argv[1].replace('x', '.')+'⟩')
    print("  Player's initial positions:", initial_state)
    print("  Bot's initial positions:", bot)
    print("  Empty cells at: ", empty)


def validate_board(initial_state, bot):
    if initial_state in algorithm.win_states():
        print("The player has already won! No point in proceeding further...")
        return False
    elif abs(len(initial_state) - len(bot)) >= 2:
        print("This is an invalid state.")
        return False
    return True


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


def analyze_result(result, initial_state, empty, size):
    total_set = set(range(size+1))
    print("\nFinal Qubits", "\t Resultant Qubit", "  Probability", "\t Steps", "\t Player's best moves")
    for probability in sorted(result.best_wins.keys(), reverse=True):
        for steps, state in result.best_wins[probability]:
            if len(result.win_moves[state]) > 0:
                final_qubit = algorithm.get_qubit(state, total_set-set(state), size)
                result_qubit = get_resulting_qubit(final_qubit, empty, set(state)-initial_state)
                print('|'+final_qubit+'⟩', '\t', '|'+result_qubit+'⟩', '\t  ', probability, '\t', steps, '\t', list(result.win_moves[state]))

    print("\nBest Player's at each board state")
    print("Previous move", '\t', 'Previous qubit state', '\t' " Next best move", '', 'Next qubit state', '', "Least #steps to win")
    for previous in list(result.player_moves.keys()):
        for each_move in result.player_moves[previous]:
            print(previous, '\t\t', '|'+each_move[0]+'⟩', '\t\t', each_move[1], '\t\t', '|'+each_move[2]+'⟩', '\t  ', each_move[3])
        print()
    #     print("\nFor previous step {%d}: " % previous)
    #     print(' ', "Next Move", "least #steps to win")
    #     moves = sorted(list(result.player_moves[previous]), key=lambda tup: tup[0])
    #     for step, move in moves:
    #         print(' ', move, '\t ', step)

    for state in result.win_circuits.keys():
        if len(result.win_circuits[state].values()) > 0:
            for circuit in result.win_circuits[state].values():
                # circuit = list(result.win_circuits[state].values())[0]
                qubit = algorithm.get_qubit(state, total_set-set(state), size)
                print("\nResultant Quantum Circuits for: ", '|'+qubit+'⟩')
                print(circuit)


def start():
    initial_state, bot, empty, size = parse_initial_state(sys.argv[1])
    max_moves = int(sys.argv[2])
    initial_log(initial_state, bot, empty)

    if validate_board(initial_state, bot):
        board = Board(initial_state, bot, size, empty, max_moves)
        your_turn = (board.size - board.empty)%2 != 0
        quantum = Quantum(initial_state, bot, size)

        for initial_seq in permutations(initial_state):
            initial_sequence = list(initial_seq)
            algorithm.initialize()
            algorithm.make_move(quantum, board, your_turn, 1, initial_sequence, 0, 0, [])
            result = algorithm.get_result(board)
            algorithm.validate_moves(result, initial_sequence)
            analyze_result(result, initial_state, empty, size)


if __name__ == '__main__':
    start()
