import chess
import pygame
import time
from pygame.locals import *
from chess.variant import *  # Importing chess variant-related modules
from chess import *  # Importing the chess module

# Constants for the graphical representation
WINDOW_WIDTH = 512
WINDOW_HEIGHT = 512
BOARD_SIZE = 8
SQUARE_SIZE = WINDOW_WIDTH // BOARD_SIZE

# Attack functions

# Function to calculate sliding attacks for a given square, occupied squares, and deltas


def custom_sliding_attacks(square: Square, occupied: Bitboard, deltas: Iterable[int]) -> Bitboard:
    attacks = BB_EMPTY  # BB_EMPTY = 0

    for delta in deltas:
        sq = square

        while True:
            sq += delta  # make sq the square the player wants to move to
            # if the square is within the board
            if not (0 <= sq < 64) or square_distance(sq, sq - delta) > 3:
                break

            attacks |= BB_SQUARES[sq]

            if occupied & BB_SQUARES[sq]:
                break

    return attacks

# Function to calculate step attacks for a given square and deltas


def custom_step_attacks(square: Square, deltas: Iterable[int]) -> Bitboard:
    return custom_sliding_attacks(square, BB_ALL, deltas)

# Function to calculate sliding attacks with a maximum distance for a given square, occupied squares, deltas, and maximum distance


def _sliding_attacks(square: Square, occupied: Bitboard, deltas: Iterable[int], max_distance: int) -> Bitboard:
    attacks = BB_EMPTY

    for delta in deltas:
        sq = square

        distance = 0  # Track the distance moved

        while True:
            sq += delta
            if not (0 <= sq < 64) or square_distance(sq, square) >= max_distance or distance >= max_distance:
                break

            attacks |= BB_SQUARES[sq]

            if occupied & BB_SQUARES[sq]:
                break

            distance += 1

    return attacks

# Function to generate an attack table for a given set of deltas


def custom_attack_table(deltas: List[int]) -> Tuple[List[Bitboard], List[Dict[Bitboard, Bitboard]]]:
    mask_table = []
    attack_table = []

    for square in SQUARES:
        attacks = {}

        mask = _sliding_attacks(square, 0, deltas, 4) & ~chess._edges(square)
        for subset in chess._carry_rippler(mask):
            attacks[subset] = _sliding_attacks(square, subset, deltas, 4)

        attack_table.append(attacks)
        mask_table.append(mask)

    return mask_table, attack_table
# Attack constants


# Pre-computed knight attacks for each square
BB_KNIGHT_ATTACKS = [custom_step_attacks(
    sq, [25, 23, 11, 5, -25, -23, -11, -5]) for sq in SQUARES]

# Pre-computed king attacks for each square
BB_KING_ATTACKS = [chess._step_attacks(sq, [8, 1, -8, -1]) for sq in SQUARES]

# Pre-computed pawn attacks for each square and color
BB_PAWN_ATTACKS = [[chess._step_attacks(
    sq, deltas) for sq in SQUARES] for deltas in [[-8], [8]]]

# Pre-computed diagonal mask and attack tables using custom deltas
BB_DIAG_MASKS, BB_DIAG_ATTACKS = custom_attack_table([-9, -7, 7, 9])

# Pre-computed file mask and attack tables using custom deltas
BB_FILE_MASKS, BB_FILE_ATTACKS = custom_attack_table([-8, 8])

# Pre-computed rank mask and attack tables using custom deltas
BB_RANK_MASKS, BB_RANK_ATTACKS = custom_attack_table([-1, 1])

# Colors
# Color for light squares on the chessboard
LIGHT_SQUARE_COLOR = (194, 209, 165)
DARK_SQUARE_COLOR = (110, 128, 93)  # Color for dark squares on the chessboard
# Color for selected square on the chessboard
SELECTED_SQUARE_COLOR = (122, 158, 196)
# Color for valid move squares on the chessboard
MOVE_SQUARE_COLOR = (100, 100, 100)

# Images for the chess pieces
PIECE_IMAGES = {
    chess.PAWN: {
        chess.WHITE: pygame.image.load("images/wp.png"),
        chess.BLACK: pygame.image.load("images/bp.png"),
    },
    chess.ROOK: {
        chess.WHITE: pygame.image.load("images/wr.png"),
        chess.BLACK: pygame.image.load("images/br.png"),
    },
    chess.KNIGHT: {
        chess.WHITE: pygame.image.load("images/wn.png"),
        chess.BLACK: pygame.image.load("images/bn.png"),
    },
    chess.BISHOP: {
        chess.WHITE: pygame.image.load("images/wb.png"),
        chess.BLACK: pygame.image.load("images/bb.png"),
    },
    chess.QUEEN: {
        chess.WHITE: pygame.image.load("images/wq.png"),
        chess.BLACK: pygame.image.load("images/bq.png"),
    },
    chess.KING: {
        chess.WHITE: pygame.image.load("images/wk.png"),
        chess.BLACK: pygame.image.load("images/bk.png"),
    },
    chess.KNIGHT: {
        chess.WHITE: pygame.image.load("images/wk.png"),
        chess.BLACK: pygame.image.load("images/bk.png"),
    },
}


class CustomBoard(chess.variant.RacingKingsBoard):
    aliases = ["Survive the Savanna", "Savanna"]
    uci_variant = "survivethesavanna"
    xboard_variant = "survivethesavanna"
    starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    def __init__(self, fen: Optional[str] = starting_fen, chess960: bool = False) -> None:
        super().__init__(fen, chess960=chess960)

    def reset(self) -> None:
        # Resets the board to the starting position
        self.set_fen(type(self).starting_fen)

    def is_variant_end(self) -> bool:
        # Checks if the variant end condition is met
        RANK8 = (chess.A8, chess.B8, chess.C8, chess.D8,
                 chess.E8, chess.F8, chess.G8, chess.H8)
        RANK1 = (chess.A1, chess.B1, chess.C1, chess.D1,
                 chess.E1, chess.F1, chess.G1, chess.H1)
        if self.king(chess.WHITE) in RANK8:
            return True
        if self.king(chess.BLACK) in RANK1:
            return True

    def attacks_mask(self, square: Square) -> Bitboard:
        # Returns the attack bitboard for a given square
        bb_square = BB_SQUARES[square]

        if bb_square & self.pawns:
            # If the square is occupied by a pawn
            color = bool(bb_square & self.occupied_co[WHITE])
            return BB_PAWN_ATTACKS[color][square]
        elif bb_square & self.knights:
            # If the square is occupied by a knight
            return BB_KNIGHT_ATTACKS[square]
        elif bb_square & self.kings:
            # If the square is occupied by a king
            return BB_KING_ATTACKS[square]
        else:
            # If the square is occupied by a bishop or queen
            attacks = 0
            if bb_square & self.bishops or bb_square & self.queens:
                attacks = BB_DIAG_ATTACKS[square][BB_DIAG_MASKS[square]
                                                  & self.occupied]
            if bb_square & self.rooks or bb_square & self.queens:
                attacks |= (BB_RANK_ATTACKS[square][BB_RANK_MASKS[square] & self.occupied] |
                            BB_FILE_ATTACKS[square][BB_FILE_MASKS[square] & self.occupied])
            return attacks

    def _attackers_mask(self, color: Color, square: Square, occupied: Bitboard) -> Bitboard:
        # Returns the attackers bitboard for a given color, square, and occupied squares
        rank_pieces = BB_RANK_MASKS[square] & occupied
        file_pieces = BB_FILE_MASKS[square] & occupied
        diag_pieces = BB_DIAG_MASKS[square] & occupied

        queens_and_rooks = self.queens | self.rooks
        queens_and_bishops = self.queens | self.bishops

        attackers = (
            (BB_KING_ATTACKS[square] & self.kings) |
            (BB_KNIGHT_ATTACKS[square] & self.knights) |
            (BB_RANK_ATTACKS[square][rank_pieces] & queens_and_rooks) |
            (BB_FILE_ATTACKS[square][file_pieces] & queens_and_rooks) |
            (BB_DIAG_ATTACKS[square][diag_pieces] & queens_and_bishops) |
            (BB_PAWN_ATTACKS[not color][square] & self.pawns))

        return attackers & self.occupied_co[color]

    def generate_pseudo_legal_moves(self, from_mask: Bitboard = BB_ALL, to_mask: Bitboard = BB_ALL) -> Iterator[Move]:
        # Generates pseudo-legal moves from a given from_mask and to_mask
        our_pieces = self.occupied_co[self.turn]

        # Generate piece moves.
        non_pawns = our_pieces & ~self.pawns & from_mask
        for from_square in scan_reversed(non_pawns):
            moves = self.attacks_mask(from_square) & ~our_pieces & to_mask
            for to_square in scan_reversed(moves):
                yield Move(from_square, to_square)

        # Generate castling moves.
        if from_mask & self.kings:
            yield from self.generate_castling_moves(from_mask, to_mask)

        # The remaining moves are all pawn moves.
        pawns = self.pawns & self.occupied_co[self.turn] & from_mask
        if not pawns:
            return

        # Generate pawn captures.
        capturers = pawns
        for from_square in scan_reversed(capturers):
            targets = (
                BB_PAWN_ATTACKS[self.turn][from_square] &
                self.occupied_co[not self.turn] & to_mask)

            for to_square in scan_reversed(targets):
                if square_rank(to_square) in [0, 7]:
                    yield Move(from_square, to_square, QUEEN)
                    yield Move(from_square, to_square, ROOK)
                    yield Move(from_square, to_square, BISHOP)
                    yield Move(from_square, to_square, KNIGHT)
                else:
                    yield Move(from_square, to_square)

        # Prepare pawn advance generation.
        if self.turn == WHITE:
            single_moves = pawns << 8 & ~self.occupied
            double_moves = single_moves << 8 & ~self.occupied & (
                BB_RANK_3 | BB_RANK_4)
        else:
            single_moves = pawns >> 8 & ~self.occupied
            double_moves = single_moves >> 8 & ~self.occupied & (
                BB_RANK_6 | BB_RANK_5)

        single_moves &= to_mask
        double_moves &= to_mask

        # Generate single pawn moves.
        for to_square in scan_reversed(single_moves):
            from_square = to_square + (8 if self.turn == BLACK else -8)

            if square_rank(to_square) in [0, 7]:
                yield Move(from_square, to_square, QUEEN)
                yield Move(from_square, to_square, ROOK)
                yield Move(from_square, to_square, BISHOP)
                yield Move(from_square, to_square, KNIGHT)
            else:
                yield Move(from_square, to_square)

        # Generate double pawn moves.
        for to_square in scan_reversed(double_moves):
            from_square = to_square + (16 if self.turn == BLACK else -16)
            yield Move(from_square, to_square)

        # Generate en passant captures.
        if self.ep_square:
            yield from self.generate_pseudo_legal_ep(from_mask, to_mask)


def draw_board(screen):
    # Draws the chessboard on the screen
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if (row + col) % 2 == 0:
                color = LIGHT_SQUARE_COLOR
            else:
                color = DARK_SQUARE_COLOR
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE,
                             row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def draw_pieces(screen, board):
    # Draws the chess pieces on the screen based on the current board state
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            square = chess.square(col, BOARD_SIZE - row - 1)
            piece = board.piece_at(square)
            if piece is not None:
                piece_image = PIECE_IMAGES[piece.piece_type][piece.color]
                screen.blit(
                    piece_image, (col * SQUARE_SIZE, row * SQUARE_SIZE))


def get_square(pos):
    # Converts a screen position to a chess square
    row = pos[1] // SQUARE_SIZE
    col = pos[0] // SQUARE_SIZE
    return chess.square(col, BOARD_SIZE - row - 1)


def main():
    # Initialize pygame and create the game window
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Chess Game")

    # Create a clock object to control the frame rate
    clock = pygame.time.Clock()

    # Create the chessboard object
    board = CustomBoard()

    # Initialize variables for handling user input and game state
    selected_square = None
    gameover = False
    winner_text = None  # Text to display the winner
    end_time = None  # End time for displaying the winner

    # Main game loop
    while not gameover:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    square = get_square(pos)
                    if selected_square is None:
                        if board.piece_at(square) is not None:
                            selected_square = square
                    else:
                        move = chess.Move(selected_square, square)
                        if board.piece_at(selected_square).piece_type == chess.PAWN and chess.square_rank(square) in [0, 7]:
                            move = chess.Move(
                                selected_square, square, promotion=chess.QUEEN)
                        if move in board.legal_moves:
                            board.push(move)
                        selected_square = None

        screen.fill((255, 255, 255))
        draw_board(screen)
        draw_pieces(screen, board)

        if selected_square is not None:
            # Add alpha value to the color tuple
            transparent_color = (*SELECTED_SQUARE_COLOR, 150)

            # Create a surface with per-pixel alpha
            rect_surface = pygame.Surface(
                (SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(rect_surface, transparent_color,
                             rect_surface.get_rect())

            # Blit the rectangle surface onto the main surface
            screen.blit(rect_surface, (chess.square_file(selected_square) * SQUARE_SIZE,
                                       (BOARD_SIZE - chess.square_rank(selected_square) - 1) * SQUARE_SIZE))

            possible_moves = []
            for move in board.legal_moves:
                if move.from_square == selected_square:
                    start_square = move.from_square
                    end_square = move.to_square
                    possible_moves.append((start_square, end_square))

            for move in possible_moves:
                move_square = move[1]
                alpha_surface = pygame.Surface(
                    (SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                circle_color = (*MOVE_SQUARE_COLOR, 200)
                circle_center = (SQUARE_SIZE // 2, SQUARE_SIZE // 2)
                circle_radius = SQUARE_SIZE // 8
                pygame.draw.circle(alpha_surface, circle_color,
                                   circle_center, circle_radius)
                screen.blit(alpha_surface, (chess.square_file(move_square) * SQUARE_SIZE,
                                            (7 - chess.square_rank(move_square)) * SQUARE_SIZE))

        pygame.display.flip()
        clock.tick(60)

        # Check if the game has ended
        if board.is_variant_end():
            result = board.result()
            if result == "1-0":
                winner_text = "White wins!"
            elif result == "0-1":
                winner_text = "Black wins!"
            else:
                winner_text = "It's a draw!"
            end_time = time.time() + 5  # Display winner for 5 seconds

        # Display the winner text and wait for 5 seconds
        if winner_text:
            font = pygame.font.Font(None, 36)
            text = font.render(winner_text, True, (0, 0, 0))
            text_rect = text.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()
            time.sleep(5)

        # Check if the time for displaying the winner has elapsed
        if end_time and time.time() >= end_time:
            gameover = True

    return
