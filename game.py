from pieces import Pawn, King

class Game:
    def __init__(self, board):
        self.board = board
        self.current_turn = 'white'
        self.in_check = False
        self.in_checkmate = False
        self.en_passant_target = None  # (x, y) of square where en passant capture can happen

    def find_king(self, color):
        """Find the position of the king for the given color"""
        for row in range(8):
            for col in range(8):
                tile = self.board.grid[row][col]
                if (tile.piece and
                    isinstance(tile.piece, King) and
                    tile.piece.color == color):
                    return (col, row)
        return None

    def is_in_check(self, color):
        # Check if the king of the given color is in check
        king_position = self.find_king(color)
        if not king_position:
            return False

        for row in self.board.grid:
            for tile in row:
                if tile.piece and tile.piece.color != color:
                    if tile.piece.is_valid_move(tile.x, tile.y, king_position[0], king_position[1], self.board):
                        return True
        return False

    def is_checkmate(self, color):
        # Check if the king of the given color is in checkmate
        if not self.is_in_check(color):
            return False

        for row in self.board.grid:
            for tile in row:
                if tile.piece and tile.piece.color == color:
                    for target_row in self.board.grid:
                        for target in target_row:
                            if tile.piece.is_valid_move(tile.x, tile.y, target.x, target.y, self.board):
                                # Temporarily move the piece to see if it resolves check
                                original_piece = target.piece
                                target.piece = tile.piece
                                tile.piece = None

                                if not self.is_in_check(color):
                                    # Restore the original piece
                                    tile.piece = target.piece
                                    target.piece = original_piece
                                    return False

                                # Restore the original piece
                                tile.piece = target.piece
                                target.piece = original_piece
        return True

    def make_move(self, start_pos, end_pos):
        start_tile = self.board.get_tile(start_pos)
        end_tile = self.board.get_tile(end_pos)

        if start_tile.piece and start_tile.piece.color == self.current_turn:
            # Check if this is an en passant move
            is_en_passant = (isinstance(start_tile.piece, Pawn) and
                           self.en_passant_target and
                           end_pos == self.en_passant_target)

            if start_tile.piece.is_valid_move(start_tile.x, start_tile.y, end_tile.x, end_tile.y, self.board) or is_en_passant:
                # Handle en passant capture
                captured_piece = None
                if is_en_passant:
                    # Remove the captured pawn (it's not on the end_tile, but adjacent)
                    captured_pawn_y = start_tile.y  # Same row as the capturing pawn
                    captured_piece = self.board.grid[captured_pawn_y][end_tile.x].piece
                    self.board.grid[captured_pawn_y][end_tile.x].piece = None

                # Move the piece
                original_end_piece = end_tile.piece
                end_tile.piece = start_tile.piece
                start_tile.piece = None

                # Check for check or checkmate
                if self.is_in_check(self.current_turn):
                    # Undo the move if it results in check
                    start_tile.piece = end_tile.piece
                    end_tile.piece = original_end_piece
                    # Restore captured piece if it was en passant
                    if captured_piece:
                        captured_pawn_y = start_pos[1]  # Original row of capturing pawn
                        self.board.grid[captured_pawn_y][end_pos[0]].piece = captured_piece
                    return False

                # Update en passant target for next turn
                self.en_passant_target = None
                if (isinstance(end_tile.piece, Pawn) and
                    abs(start_pos[1] - end_pos[1]) == 2):
                    # Pawn moved two squares, set en passant target
                    en_passant_y = (start_pos[1] + end_pos[1]) // 2
                    self.en_passant_target = (end_pos[0], en_passant_y)

                # Mark pawn as moved
                if isinstance(end_tile.piece, Pawn):
                    end_tile.piece.has_moved = True

                # Switch turns
                self.current_turn = 'black' if self.current_turn == 'white' else 'white'
                return True

        return False

    def show_status(self):
        if self.in_check:
            print(f"{self.current_turn.capitalize()} is in check!")
        if self.in_checkmate:
            print(f"{self.current_turn.capitalize()} is in checkmate!")
        else:
            print(f"{self.current_turn.capitalize()}'s turn.")