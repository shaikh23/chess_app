class Piece:
    def __init__(self, color):
        self.color = color

    def is_valid_move(self, from_x, from_y, to_x, to_y, board):
        """Check if a move is valid for this piece type"""
        pass

    def get_possible_moves(self, x, y, board):
        """Get all possible moves from current position"""
        return []

class Pawn(Piece):
    # also need to include logic for en passant and promotion
    # en passant allows a pawn to capture an opponent's pawn that has moved two squares forward
    def __init__(self, color):
        super().__init__(color)
        self.has_moved = False

    def is_valid_move(self, from_x, from_y, to_x, to_y, board):
        direction = -1 if self.color == 'white' else 1  # White moves up (-1), black moves down (+1)

        # Forward move
        if from_x == to_x:  # Same column
            if to_y == from_y + direction:  # One square forward
                return board.grid[to_y][to_x].piece is None
            elif to_y == from_y + 2 * direction and not self.has_moved:  # Two squares forward on first move
                return (board.grid[to_y][to_x].piece is None and
                       board.grid[from_y + direction][to_x].piece is None)

        # Diagonal capture (regular or en passant)
        elif abs(from_x - to_x) == 1 and to_y == from_y + direction:
            target_piece = board.grid[to_y][to_x].piece
            # Regular diagonal capture
            if target_piece is not None and target_piece.color != self.color:
                return True
            # En passant capture - check if there's a game instance with en_passant_target
            # This will be validated by the Game class
            return target_piece is None  # Allow move to empty square for en passant

        return False


class Rook(Piece):
    def is_valid_move(self, from_x, from_y, to_x, to_y, board):
        # Rook moves horizontally or vertically
        if from_x != to_x and from_y != to_y:
            return False

        return self._is_path_clear(from_x, from_y, to_x, to_y, board)

    def _is_path_clear(self, from_x, from_y, to_x, to_y, board):
        """Check if path is clear between two points"""
        dx = 0 if from_x == to_x else (1 if to_x > from_x else -1)
        dy = 0 if from_y == to_y else (1 if to_y > from_y else -1)

        x, y = from_x + dx, from_y + dy
        while x != to_x or y != to_y:
            if board.grid[y][x].piece is not None:
                return False
            x += dx
            y += dy

        # Check destination square
        target_piece = board.grid[to_y][to_x].piece
        return target_piece is None or target_piece.color != self.color


class Knight(Piece):
    def is_valid_move(self, from_x, from_y, to_x, to_y, board):
        # Knight moves in L-shape: 2 squares in one direction, 1 in perpendicular
        dx = abs(to_x - from_x)
        dy = abs(to_y - from_y)

        if not ((dx == 2 and dy == 1) or (dx == 1 and dy == 2)):
            return False

        # Check destination square
        target_piece = board.grid[to_y][to_x].piece
        return target_piece is None or target_piece.color != self.color


class Bishop(Piece):
    def is_valid_move(self, from_x, from_y, to_x, to_y, board):
        # Bishop moves diagonally
        dx = abs(to_x - from_x)
        dy = abs(to_y - from_y)

        if dx != dy:  # Not diagonal
            return False

        return self._is_diagonal_path_clear(from_x, from_y, to_x, to_y, board)

    def _is_diagonal_path_clear(self, from_x, from_y, to_x, to_y, board):
        """Check if diagonal path is clear"""
        dx = 1 if to_x > from_x else -1
        dy = 1 if to_y > from_y else -1

        x, y = from_x + dx, from_y + dy
        while x != to_x or y != to_y:
            if board.grid[y][x].piece is not None:
                return False
            x += dx
            y += dy

        # Check destination square
        target_piece = board.grid[to_y][to_x].piece
        return target_piece is None or target_piece.color != self.color


class Queen(Piece):
    def is_valid_move(self, from_x, from_y, to_x, to_y, board):
        # Queen combines rook and bishop movement
        # Horizontal/vertical movement
        if from_x == to_x or from_y == to_y:
            return self._is_path_clear(from_x, from_y, to_x, to_y, board)

        # Diagonal movement
        dx = abs(to_x - from_x)
        dy = abs(to_y - from_y)
        if dx == dy:
            return self._is_diagonal_path_clear(from_x, from_y, to_x, to_y, board)

        return False

    def _is_path_clear(self, from_x, from_y, to_x, to_y, board):
        """Check if horizontal/vertical path is clear"""
        dx = 0 if from_x == to_x else (1 if to_x > from_x else -1)
        dy = 0 if from_y == to_y else (1 if to_y > from_y else -1)

        x, y = from_x + dx, from_y + dy
        while x != to_x or y != to_y:
            if board.grid[y][x].piece is not None:
                return False
            x += dx
            y += dy

        target_piece = board.grid[to_y][to_x].piece
        return target_piece is None or target_piece.color != self.color

    def _is_diagonal_path_clear(self, from_x, from_y, to_x, to_y, board):
        """Check if diagonal path is clear"""
        dx = 1 if to_x > from_x else -1
        dy = 1 if to_y > from_y else -1

        x, y = from_x + dx, from_y + dy
        while x != to_x or y != to_y:
            if board.grid[y][x].piece is not None:
                return False
            x += dx
            y += dy

        target_piece = board.grid[to_y][to_x].piece
        return target_piece is None or target_piece.color != self.color


class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.has_moved = False

    def is_valid_move(self, from_x, from_y, to_x, to_y, board):
        dx = abs(to_x - from_x)
        dy = abs(to_y - from_y)

        # King moves one square in any direction
        if dx <= 1 and dy <= 1 and (dx != 0 or dy != 0):
            target_piece = board.grid[to_y][to_x].piece
            return target_piece is None or target_piece.color != self.color

        # TODO: Add castling logic here if needed
        return False