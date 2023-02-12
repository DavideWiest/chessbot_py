import numpy

from .move import *

class Figure():
    """
    Chess figure
    moveLen = Number of moves in each moveDirection
    moveDirections = Change in x,y position of the figure, third element = if piece needs to be
    """

    def getLegalMovesByBoard(self, board: numpy.ndarray, position: tuple, side: int):
        allmoves = self.allMoves.copy()
        allmoves2 = [
            (x,y) for x,y in allmoves if 0 < position[0]+y < 8 and 0 < position[1]+x < 8
        ]

        moves = [
            (x,y) for x,y in allmoves2 if board[position[0]+y, position[1]+x, side] == 0
        ]

        return moves

    def __repr__(self):
        return PIECES_ID_TO_STR[PIECES_CLASS_TO_ID[self.__class__.__name__]]

class King(Figure):
    def __init__(self):
        self.allMoves = [
            (x,y) for x in range(-1,2) for y in range(-1,2)
        ]
        while (0,0) in self.allMoves:
            self.allMoves.remove((0,0))

    def getLegalMoves(self, board: numpy.ndarray, position: tuple, side: int, piecesPos: dict, pieceId: int, pieceIndex: int, level: int=1):

        # to implement

        moves = self.getLegalMovesByBoard(board, position, side)

        # castling
        startPos = (0 if side==0 else 7, 3)

        # if king and rook in startposition, and none of the spaces in between are occupied
        if position == startPos and \
            board[startPos[0], 0, side] == ROOK and \
            allIdInBoardRange(board, startPos[0], (1,3), (0,1), 0):
            moves.append((startPos[0], 1))
        
        if position == startPos and \
            board[startPos[0], 7, side] == ROOK and \
            allIdInBoardRange(board, startPos[0], (4,7), (0,1), 0):
            moves.append((startPos[0], 6))

        if level == 1:
            moves = filterForCheckNextMove(board, moves, position, side, piecesPos, pieceId, pieceIndex)

        return [
            (position[0]+y, position[1]+x) for x,y in moves
        ]


class Queen(Figure):
    def __init__(self):
        self.allMoves = [
            (x,0) for x in range(-7,8)
        ] + [
            (0,y) for y in range(-7,8)
        ] + [
            (x*d1,x*d2) for x in range(0,8)
            for d1 in [-1, 1] for d2 in [-1,1]
        ]
        while (0,0) in self.allMoves:
            self.allMoves.remove((0,0))

    def getLegalMoves(self, board: numpy.ndarray, position: tuple, side: int, piecesPos: dict, pieceId: int, pieceIndex: int, level: int=1):

        moves = self.getLegalMovesByBoard(board, position, side)

        # sort out moves that are blocked

        moves = filterStraight(board, moves, position, side)
        moves = filterDiagonally(board, moves, position, side)

        if level == 1:
            moves = filterForCheckNextMove(board, moves, position, side, piecesPos, pieceId, pieceIndex)

        return [
            (position[0]+y, position[1]+x) for x,y in moves
        ]

class Pawn(Figure):
    def __init__(self):
        self.allMoves = [
            (-1,1), (0,1), (1,1)
        ]
        while (0,0) in self.allMoves:
            self.allMoves.remove((0,0))

    def getLegalMoves(self, board: numpy.ndarray, position: tuple, side: int, piecesPos: dict, pieceId: int, pieceIndex: int, level: int=1, lastMove: Move = (-1,-1)):

        moves = self.getLegalMovesByBoard(board, position, side)

        # pawns can only move downwards if side == white else only upwards
        sideDir = DIRECTION(side)
        moves = [
            (x,sideDir*y) for x,y in moves
        ]

        if (-1,sideDir*1) in moves:
            if board[position[0]+sideDir*1, position[1]-1, OTHERSIDE(side)] == 0:
                moves.remove((-1,sideDir*1))

                # en passant
                if board[position[0], position[1]-1, OTHERSIDE(side)] == PAWN and lastMove.x == position[0]+1 and lastMove.y == position[1]:
                    moves.append((1,sideDir*1))

        if (1,sideDir*1) in moves:
            if board[position[0]+sideDir*1, position[1]+1, OTHERSIDE(side)] == 0:
                moves.remove((1,sideDir*1))
            
                # en passant    
                if board[position[0], position[1]+1, OTHERSIDE(side)] == PAWN and lastMove.x == position[0]+1 and lastMove.y == position[1]:
                    moves.append((1,sideDir*1))

        # if pawn hasnt moved yet: can move 2 pieces
        startPos = 1 if side==0 else 6
        # if pawn hasnt moved yet, space is not occupied, and piece can move 1 further already
        if position[0] == startPos and \
            allIdInBoardRange(board, position[0]+sideDir*2, position[1], (0,1), 0) and \
            (0,sideDir*1) in moves:
            moves.append((0, sideDir*2))

        if level == 1:
            moves = filterForCheckNextMove(board, moves, position, side, piecesPos, pieceId, pieceIndex)

        return [
            (position[0]+y, position[1]+x) for x,y in moves
        ]

class Knight(Figure):
    def __init__(self):
        self.allMoves = [
            (2,1), (2,-1),
            (1,2), (1,-2),
            (-1,2), (-1,-2),
            (-2,1), (-2,-1)
        ]
        while (0,0) in self.allMoves:
            self.allMoves.remove((0,0))

    def getLegalMoves(self, board: numpy.ndarray, position: tuple, side: int, piecesPos: dict, pieceId: int, pieceIndex: int, level: int=1):

        moves = self.getLegalMovesByBoard(board, position, side)

        if level == 1:
            moves = filterForCheckNextMove(board, moves, position, side, piecesPos, pieceId, pieceIndex)

        return [
            (position[0]+y, position[1]+x) for x,y in moves
        ]

class Bishop(Figure):
    def __init__(self):
        self.allMoves = [
            (x*d1,x*d2) for x in range(0,8)
            for d1 in [-1, 1] for d2 in [-1,1]
        ]
        while (0,0) in self.allMoves:
            self.allMoves.remove((0,0))

    def getLegalMoves(self, board: numpy.ndarray, position: tuple, side: int, piecesPos: dict, pieceId: int, pieceIndex: int, level: int=1):

        moves = self.getLegalMovesByBoard(board, position, side)

        moves = filterDiagonally(board, moves, position, side)

        if level == 1:
            moves = filterForCheckNextMove(board, moves, position, side, piecesPos, pieceId, pieceIndex)

        return [
            (position[0]+y, position[1]+x) for x,y in moves
        ]

class Rook(Figure):
    def __init__(self):
        self.allMoves = [
            (x,0) for x in range(-7,8)
        ] + [
            (0,y) for y in range(-7,8)
        ]
        while (0,0) in self.allMoves:
            self.allMoves.remove((0,0))

    def getLegalMoves(self, board: numpy.ndarray, position: tuple, side: int, piecesPos: dict, pieceId: int, pieceIndex: int, level: int=1):

        moves = self.getLegalMovesByBoard(board, position, side)

        moves = filterStraight(board, moves, position, side)

        if level == 1:
            moves = filterForCheckNextMove(board, moves, position, side, piecesPos, pieceId, pieceIndex)

        return [
            (position[0]+y, position[1]+x) for x,y in moves
        ]

def filterDiagonally(board: numpy.ndarray, moves, position: tuple, side: int):
    for d1 in [-1,1]:
            for d2 in [-1,1]:
                blocked = False
                for x in range(0,8):
                    if (x*d1,x*d2) in moves:
                        if blocked == True:
                            moves.remove((x*d1,x*d2))
                            continue

                        if board[position[0]+x*d2, position[1]+x*d1, side] != 0:
                            moves.remove((x*d1,x*d2))
                            blocked = True

                        if board[position[0]+x*d2, position[1]+x*d1, OTHERSIDE(side)] != 0:
                            blocked = True
        
    return moves

def filterStraight(board: numpy.ndarray, moves, position: tuple, side: int):
    blockedX = False
    blockedY = False
    for xOry in range(-7,8):
        # y-moves
        if (0,xOry) in moves:
            if blockedX == True:
                moves.remove((0,xOry))
                continue

            if board[position[0]+xOry, position[1], side] != 0:
                moves.remove(((xOry,0)))
                blockedX = True

            if board[position[0]+xOry, position[1], OTHERSIDE(side)] != 0:
                blockedX = True

        # x-moves
        if (xOry,0) in moves:
            if blockedY == True:
                moves.remove((0,xOry))
                continue

            if board[position[0], position[1]+xOry, side] != 0:
                moves.remove(((0,xOry)))
                blockedY = True

            if board[position[0], position[1]+xOry, OTHERSIDE(side)] != 0:
                blockedY = True
                
    return moves

def filterForCheckNextMove(board: numpy.ndarray, moves, position: tuple, side: int, piecesPos: dict, pieceId: int, pieceIndex: int):
    position_orig = position
    moves2 = []
    for move in moves:
        position = (position_orig[0]+move[1], position_orig[1]+move[0])

        allEnemyPieces = [
            (pieceId, enemypieceIndex)
            for pieceId, piecelist in piecesPos[OTHERSIDE(side)].items() 
            for enemypieceIndex in range(len(piecelist))
        ]

        piecesPosCopy = piecesPos.copy()
        piecesPosCopy[side][pieceId][pieceIndex] = position

        board2 = board.copy()

        board2[position_orig[0], position_orig[1], side] = 0
        board2[position[0], position[1], side] = pieceId
        board2[position[0], position[1], OTHERSIDE(side)] = 0

        # testing
        print(piecesPosCopy)

        for pieceId, enemypieceIndex in allEnemyPieces:
            if not any(pieceMovePos == piecesPosCopy[side][KING][0] for pieceMovePos in PIECES_ID_TO_CLASS[pieceId].getLegalMoves(board, tuple(piecesPosCopy[OTHERSIDE(side)][pieceId][enemypieceIndex]), OTHERSIDE(side), piecesPosCopy, pieceId, enemypieceIndex, level=2)):
                moves2.append(move)

    return moves2


def allIdInBoardRange(board: numpy.ndarray, yRange, xRange, sideOneOrBoth, wantedId=0):
    """ sideOneOrBoth: int -> one side, anything else -> both sides 
        xRange, yRange: tuple: range, anything else (int) -> the one int
    """
    if isinstance(xRange, tuple):
        xRange = range(xRange[0], xRange[1])
    else:
        xRange = range(xRange, xRange+1)
    if isinstance(yRange, tuple):
        yRange = range(yRange[0], yRange[1])
    else:
        yRange = range(yRange, yRange+1)

    for x in xRange:
        for y in yRange:
            if isinstance(sideOneOrBoth, int):
                if board[x,y,sideOneOrBoth] != wantedId:
                    return False
            else:
                if board[x,y,0] != wantedId or board[x,y,1] != wantedId:
                    return False

    return True


BLACK = 0
WHITE = 1

OTHERSIDE = lambda side: WHITE if side==BLACK else BLACK
DIRECTION = lambda side: 1 if side==BLACK else -1

KING = 10
PAWN = 1
KNIGHT = 3
BISHOP = 4
ROOK = 5
QUEEN = 9

PIECES_ID_TO_CLASS = {
    KING: King(),
    PAWN: Pawn(),
    KNIGHT: Knight(),
    BISHOP: Bishop(),
    ROOK: Rook(),
    QUEEN: Queen()
}

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