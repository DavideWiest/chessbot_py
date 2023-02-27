import game
from string import ascii_lowercase

from .relations import *

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

        if piece != "p" and "=" in move_orig:
            raise ValueError

        if not posX.isnumeric():
            if posX not in ascii_lowercase[:8]:
                raise ValueError
            posX = ascii_lowercase.index(posX)
        else:
            posX = int(posX)-1

        if posY.isnumeric():
            posY = 8-int(posY)
        else:
            raise ValueError

        if posX < 0 or posX > 8:
            raise ValueError

        if posY < 0 or posX > 8:
            raise ValueError

        if piece not in PIECES_STR_TO_ID:
            raise ValueError

        piece = PIECES_STR_TO_ID[piece]

        self.original = move_orig
        self.p = piece
        self.x = posX
        self.y = posY

    def __repr__(self):
        return f"{self.original}: {PIECES_ID_TO_NAME[self.p]} to {ascii_lowercase[self.x]}{self.y+1}"
        

class MoveWithInts(Move):
    def __init__(self, p: int, x: int, y: int, side: int, piecePosition: tuple):
        "save integer move"

        self.original = convertToStrMoveXY((x,y))
        self.p = p
        self.pPos = piecePosition
        self.x = x
        self.y = y
        self.side = side


def convertToStrMoveXY(moveYX: tuple, p: int = 0):

    x = ascii_lowercase[moveYX[1]]
    y = str(8-moveYX[0])

    if p != 0:
        p = PIECES_ID_TO_STR[p]
        if p != "p":
            x = p+x

    return x+y
