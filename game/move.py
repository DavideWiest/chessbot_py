import game
from string import ascii_lowercase

class Move():

    def __init__(self, move: str, side: int, piecePosition: tuple):
        "Convert string move and validate it"

        move = move.lower()
        if len(move) not in (2,3):
            raise ValueError

        if len(move) == 3:
            piece, posX, posY = move
        else:
            piece, posX, posY = "p" + move

        if posX.isnumeric():
            if piece not in ascii_lowercase[:8]:
                raise ValueError
            posX = ascii_lowercase.index(piece)+1
        else:
            posX = int(posX)

        if posY.isnumeric():
            posY = int(posY)
        else:
            raise ValueError

        if posX < 1 or posX > 8:
            raise ValueError

        if posY < 1 or posX > 8:
            raise ValueError

        if piece.isnumeric():
            piece = int(piece)
        else:
            if piece not in game.PIECES_STR_TO_ID:
                raise ValueError

            piece = game.PIECES_STR_TO_ID[piece]

        self.original = move
        self.p = piece
        self.pPos = piecePosition
        self.x = posX
        self.y = posY
        self.side = side

    def __init__(self, p: int, x: int, y: int, side: int):
        "save integer move"

        self.p = p
        self.x = x
        self.y = y
        self.side = side


def convertToStrMoveXY(moveXY: tuple):

    x = ascii_lowercase[moveXY[0]-1]
    y = str(moveXY[1])

    return x+y