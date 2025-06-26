class Tile:
    def __init__(self, color, x, y):
        self.color = color
        self.piece = None # Placeholder for a piece on the tile
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Tile({self.color}, {self.piece})"

class Board():

    def __init__(self, size):
        self.grid = self._create_board()

    def _create_board(self):
        board = []
        for row in range(8):
            board_row = []
            for col in range(8):
                color = 'white' if (row + col) % 2 == 0 else 'black'
                tile = Tile(color, col, row)
                board_row.append(tile)
            board.append(board_row)
        return board

    def get_tile(self, pos):
        """Get tile at position (x, y)"""
        x, y = pos
        return self.grid[y][x]

    def display(self):
        for row in self.grid:
            print(' '.join(str(tile) for tile in row))