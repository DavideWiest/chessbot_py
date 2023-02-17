from colorama import Fore, Back, Style

BLACK = 0
WHITE = 1

OTHERSIDE = lambda side: WHITE if side==BLACK else BLACK
DIRECTION = lambda side: 1 if side==BLACK else -1

KING = 2
PAWN = 1
KNIGHT = 3
BISHOP = 4
ROOK = 5
QUEEN = 9


PIECES_CLASS_TO_ID = {
    "King": KING,
    "Pawn": PAWN,
    "Knight": KNIGHT,
    "Bishop": BISHOP,
    "Rook": ROOK,
    "Queen": QUEEN 
}

PIECES_STR_TO_ID = {
    "k": KING,
    "p": PAWN,
    "n": KNIGHT,
    "b": BISHOP,
    "r": ROOK,
    "q": QUEEN
}

PIECES_ID_TO_STR = {v: k for k, v in PIECES_STR_TO_ID.items()}

PAWN_PROMOTION_OPTIONS = [
    "n", "b", "r", "q"
]

COLOR_SIDE = lambda side: Fore.GREEN if side==BLACK else Fore.YELLOW
TEST_COLOR = Fore.MAGENTA