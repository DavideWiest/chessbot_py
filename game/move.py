import game
from string import ascii_lowercase

class Move():

    def __init__(self, move: str, side: int, piecePosition: tuple):
        "Convert string move and validate it"

        move_orig = move
        move = move.lower()

        self.side = side
        self.pPos = piecePosition

        if move == "o-o-o":
            self.original = move
            self.p = KING
            self.x = 1
            self.y = 0 if side == 0 else 7
            return
        elif move == "o-o":
            self.original = move
            self.p = KING
            self.x = 6
            self.y = 0 if side == 0 else 7
            return
        elif "=" in move and move.split("=")[1] in PAWN_PROMOTION_OPTIONS:
            move = move.split("=")[0]
        

        if len(move) not in (2,3):
            raise ValueError

        if len(move) == 3:
            piece, posX, posY = move
        else:
            piece, posX, posY = "p" + move

        if posX.isnumeric():
            if piece not in ascii_lowercase[:8]:
                raise ValueError
            posX = ascii_lowercase.index(piece)
        else:
            posX = int(posX)-1

        if posY.isnumeric():
            posY = int(posY)-1
        else:
            raise ValueError

        if posX < 0 or posX > 8:
            raise ValueError

        if posY < 0 or posX > 8:
            raise ValueError

        if piece.isnumeric():
            piece = int(piece)
        else:
            if piece not in game.PIECES_STR_TO_ID:
                raise ValueError

            piece = game.PIECES_STR_TO_ID[piece]

        self.original = move_orig
        self.p = piece
        self.x = posX
        self.y = posY
        

class MoveWithInts(Move):
    def __init__(self, p: int, x: int, y: int, side: int, piecePosition: tuple):
        "save integer move"

        self.original = convertToStrMoveXY((x,y))
        self.p = p
        self.pPos = piecePosition
        self.x = x
        self.y = y
        self.side = side


def convertToStrMoveXY(moveXY: tuple, p: int = 0):

    x = ascii_lowercase[moveXY[0]]
    y = str(moveXY[1])

    if p != 0:
        p = PIECES_ID_TO_STR[p]
        if p != "p":
            x = p+x

    return x+y

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