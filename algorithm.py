import copy
import random
from models import LOGGING, Board
from collections import defaultdict

best_wins = defaultdict(set)
win_moves = defaultdict(set)


def get_qubit(state, bot, size):
    qubit = ''
    for i in range(size):
        if i+1 in state:
            qubit += '1'
        elif i+1 in bot:
            qubit += '0'
        else:
            qubit += 'x'
    return qubit


def win_states():
    """
    Min positions of 1 for a win
    """
    win_states = set()
    win_states.add(tuple([1,2,3]))
    win_states.add(tuple([1,5,9]))
    win_states.add(tuple([1,4,7]))
    win_states.add(tuple([4,5,6]))
    win_states.add(tuple([2,5,8]))
    win_states.add(tuple([3,6,9]))
    win_states.add(tuple([7,8,9]))
    win_states.add(tuple([3,5,7]))
    return win_states


def get_all_possible_states(board, turn):
    """
    Given a state, get all possible moves and their probability
    This is the brute force algorithm

    TODO: optimizing player's move, by getting only the next states with the highest probability
    next_states,next_probability = get_probable_next_states(board, next_states)
    """
    next_states = []
    next_probability = float(pow(board.empty, -1))
    for pos in board.available:
        next_state = set()
        if turn == 'player':
            next_state = board.state.copy()
        else:
            next_state = board.bot.copy()
        # TODO: replace this with Quantum gate Algorithm, to set qubit to |1>, when it's player's turn
        next_state.add(pos)
        next_states.append((pos, next_state))
    return next_states, next_probability


def evaluate_penultimate_state(board, probability, moves, steps):
    """
    If it's the penultimate state,
    return True if the given state is a win state for the player
    """
    win = False
    for win_pos in win_states():
        if set(win_pos).issubset(board.state):
            if steps <= board.max:
                best_wins[probability].add(tuple([steps, tuple(board.state)]))
                win_moves[tuple(board.state)].add(tuple(moves))
            win = True
            break
    return win


def player_move(board, current_probability, moves, steps, steps_bot):

    total_steps = steps + steps_bot

    if LOGGING:
        print()
        print('\t'*total_steps, "Player's move now...")
        print('\t'*total_steps, "Player's moves so far: ", moves)

    next_states, next_probability = get_all_possible_states(board, 'player')
    new_probability = float(next_probability * current_probability)
    best_probability = 0
    total_probability = 0
    best_move = 0

    if LOGGING:
        print('\t'*total_steps, "(%d) total possible next states, each with probability (%.4f)" % (len(next_states), next_probability))

    for pos, next_state in next_states:
        new_empty_cells = board.available.copy()
        new_empty_cells.remove(pos)
        new_board = Board(next_state, board.bot, board.size, new_empty_cells, board.max)
        next_move = pos
        local_probability = 0

        if LOGGING:
            print()
            print('\t'*total_steps, "################## NEW PLAYER BRANCH ##################")
            print('\t'*total_steps, "Player's next move at (%d) with probability: (%.4f)" % (next_move, new_probability))
            print('\t'*total_steps, "New qubit state: ", '|'+get_qubit(new_board.state, new_board.bot, board.size)+'⟩')
            print('\t'*total_steps, "Empty cells at: ", new_board.available)

        if evaluate_penultimate_state(new_board, new_probability, moves+[next_move], steps+1):
            local_probability += new_probability
            if LOGGING:
                print('\t'*total_steps, "Congrats! This is a WIN!")
        elif new_board.empty > 1:
            temp_probability = make_move(new_board, (new_board.size - new_board.empty)%2 != 0, new_probability, moves+[next_move], steps+1, steps_bot)
            if LOGGING:
                print('\t'*total_steps, temp_probability)
            if temp_probability > 0:
                local_probability += temp_probability
        elif evaluate_penultimate_state(new_board, new_probability, moves+[next_move], steps+1):
                local_probability += new_probability
                if LOGGING:
                    print('\t'*total_steps, "Congrats! This is a WIN!")

        total_probability += local_probability
        if local_probability > best_probability:
            best_move = next_move
            best_probability = local_probability

        if LOGGING:
            print()
            print('\t'*total_steps, "Total win probability for move (%d) at step (%d) = (%.4f)" % (next_move, steps+1, local_probability))

    if LOGGING:
        print()
        if best_probability > 0:

            # TODO: replace qubit setting here. Only set a qubit if there is a best win probability
            print('\t'*total_steps, "The best move is (%d), which has a best win probability of (%.4f)" % (best_move, best_probability))
        else:
            print('\t'*total_steps, "No wins for the player here")
        print('\t'*total_steps, "#######################################################")

    return total_probability


def bot_move(board, current_probability, moves, steps, steps_bot):
    """
    In this case, the bot need not do anything,
    because the default qubit is |0>, and so
    it only has to borrow an extra qubit at a random position
    """
    total_steps = steps + steps_bot

    if LOGGING:
        print()
        print('\t'*total_steps,"Bot's move now...")

    next_states, next_probability = get_all_possible_states(board, 'bot')
    best_probability = 0

    for pos, next_state in next_states:
        new_empty_cells = board.available.copy()
        new_empty_cells.remove(pos)
        next_move = pos
        new_board = Board(board.state, next_state, board.size, new_empty_cells, board.max)
        local_probability = 0

        if LOGGING:
            print()
            print('\t'*total_steps,"------------------ NEW BOT BRANCH ------------------")
            print('\t'*total_steps,"Bot's next move at (%d)" % next_move)
            print('\t'*total_steps,"New qubit state: ", '|'+get_qubit(new_board.state, new_board.bot, board.size)+'⟩')
            print('\t'*total_steps,"Empty cells at: ", new_board.available)

        if new_board.empty > 0:
            temp_probability = make_move(new_board, (new_board.size - new_board.empty)%2 != 0, current_probability, moves, steps, steps_bot+1)
            if LOGGING:
                print('\t'*total_steps, temp_probability)
            local_probability += temp_probability

        best_probability = max(best_probability, local_probability)

    return best_probability


def make_move(board, your_turn, current_probability, moves, steps, steps_bot):
    return player_move(board, current_probability, moves, steps, steps_bot) if your_turn else bot_move(board, current_probability, moves, steps, steps_bot)


def get_result(board):
    return best_wins, win_moves
