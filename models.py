
LOGGING = False

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
