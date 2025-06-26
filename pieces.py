class Piece:
    def __init__(self, color):
        self.color = color

    def move(self, x, y):
        pass

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.has_moved = False

    def move(self, x, y):
        if not self.has_moved:
            # Logic for first move (can move two squares)
            pass
        else:
            # Logic for normal move (one square)
            pass
        self.has_moved = True


class Rook(Piece):


class Knight(Piece):


class Bishop(Piece):


class Queen(Piece):


class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.has_moved = False

    def move(self, x, y):
        # Logic for king's move
        if not self.has_moved:
            # Logic for castling
            pass
        self.has_moved = True