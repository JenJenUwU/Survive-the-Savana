from chess import *
import chess
def _attack_table(deltas: List[int]) -> Tuple[List[Bitboard], List[Dict[Bitboard, Bitboard]]]:
    mask_table = []
    attack_table = []

    for square in SQUARES:
        attacks = {}

        mask = chess._sliding_attacks(square, 0, deltas) & ~chess._edges(square)
        # store the sliding attacks for all squares on the chessboard, taking into account their adjacency to the edges.
        print(mask)
        print("")
        for subset in chess._carry_rippler(mask):
            attacks[subset] = chess._sliding_attacks(square, subset, deltas)

        attack_table.append(attacks)
        mask_table.append(mask)

    return mask_table, attack_table
_attack_table([8,-8])