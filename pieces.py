import chess

class CustomPiece(chess.Piece):
    def __init__(self, piece_type, color):
        super().__init__(piece_type, color)

    def __str__(self):
        if self.piece_type == chess.PAWN:
            return "X" if self.color == chess.WHITE else "x"
        else:
            return super().__str__()

    def generate_legal_moves(self, from_square):
        # Get the standard knight moves
        knight_moves = chess.SquareSet.from_square(from_square).knight()

        # Modify the knight moves to include the custom movement pattern
        custom_moves = set()
        for move in knight_moves:
            custom_moves.add(move + 3 * chess.SQUARES_PER_RANK)

        return custom_moves

# Create a custom chessboard with the custom piece
custom_board = chess.Board()
custom_board.set_piece_at(chess.A1, CustomPiece(chess.PAWN, chess.WHITE))

# Play the game with the custom piece
move = chess.Move.from_uci("a1c2")  # Custom piece moves like knight but with modified pattern
custom_board.push(move)
