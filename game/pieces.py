from board import ChessBoard
import numpy

from move import *

class Figure():
    """
    Chess figure
    moveLen = Number of moves in each moveDirection
    moveDirections = Change in x,y position of the figure, third element = if piece needs to be
    """

    def getLegalMovesByBoard(self, board: numpy.ndarray, position: tuple, side: int):
        allmoves = self.allMoves.copy()
        allmoves2 = [
            (x,y) for x,y in allmoves if 0 < position[0]+x < 9 and 0 < position[1]+y < 9
        ]

        moves = [
            (x,y) for x,y in moves if board[position[0]+x, position[1]+y, side] == 0
        ]

        return allmoves2

    def __repr__(self):
        return PIECES_ID_TO_STR[PIECES_CLASS_TO_ID[self.__class__.__name__]]

class King(Figure):
    def __init__(self):
        self.allMoves = [
            (x,y) for x in range(-1,2) for y in range(-1,2)
        ]
        while (0,0) in self.allMoves:
            self.allMoves.remove((0,0))

    def hasAnyProtection(self, board: numpy.ndarray, position: tuple, side: int, piecesPos: dict):
        
        allEnemyPieces = [
            (pieceId, position)
            for pieceId, piecelist in piecesPos[1 if side==0 else 0].items() 
            for position in piecelist
        ]

        for pieceId, position in allEnemyPieces:
            if pieceId != 10:
                if any(pieceMovePos == position for pieceMovePos in PIECES_ID_TO_CLASS[pieceId].getLegalMoves(board, tuple(position), 1 if side==0 else 0)):
                    return True

    def getLegalMoves(self, board: numpy.ndarray, position: tuple, side: int, piecesPos: dict, ignorePos: tuple):

        # to implement

        moves = self.getLegalMovesByBoard(board, position, side)

        movesThreateningEnemy = [
            (x,y) for x,y in moves if board[position[0]+x, position[1]+y, 1 if side==0 else 0] != 0
        ]

        movesIllegalByCover = [
            (x,y) for x,y in movesThreateningEnemy if self.hasAnyProtection(board, (position[0]+x, position[1]+y), side, piecesPos)
        ]

        moves = [
            (x,y) for x,y in moves if (x,y) not in movesIllegalByCover
        ]

        return [
            (position[0]+x, position[1]+y) for x,y in moves
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

    def getLegalMoves(self, board: numpy.ndarray, position: tuple, side: int, ignorePos: tuple):

        moves = self.getLegalMovesByBoard(board, position, side)

        # sort out moves that are blocked

        moves = filterStraight(board, moves, position, side)
        moves = filterDiagonally(board, moves, position, side)

        return [
            (position[0]+x, position[1]+y) for x,y in moves
        ]

class Pawn(Figure):
    def __init__(self):
        self.allMoves = [
            (-1,1), (0,1), (1,1)
        ]
        while (0,0) in self.allMoves:
            self.allMoves.remove((0,0))

    def getLegalMoves(self, board: numpy.ndarray, position: tuple, side: int, ignorePos: tuple, lastMove: Move):

        moves = self.getLegalMovesByBoard(board, position, side)

        # pawns can only move downwards if side == white else only upwards
        sideDir = -1 if side==0 else 1
        moves = [
            (x,sideDir*y) for x,y in moves
        ]

        if (-1,sideDir*1) in moves:
            if board[position[0]-1, position[1]+sideDir*1, 1 if side==0 else 1] == 0:
                moves.remove((-1,sideDir*1))

                # en passant
                if board[position[0]+1, position[1], 1 if side==0 else 1] == 1 and lastMove.x == position[0]+1 and lastMove.y == position[1]:
                    moves.add((1,sideDir*1))

        if (1,sideDir*1) in moves:
            if board[position[0]+1, position[1], 1 if side==0 else 1] == 0:
                moves.remove((1,sideDir*1))
            
                # en passant    
                if board[position[0]+1, position[1], 1 if side==0 else 1] == 1 and lastMove.x == position[0]+1 and lastMove.y == position[1]:
                    moves.add((1,sideDir*1))

        return [
            (position[0]+x, position[1]+y) for x,y in moves
        ]

class Knight(Figure):
    def getLegalMoves(self, board: numpy.ndarray, position: tuple, side: int, ignorePos: tuple):

        moves = self.getLegalMovesByBoard(board, position, side)

        return [
            (position[0]+x, position[1]+y) for x,y in moves
        ]

class Bishop(Figure):
    def __init__(self):
        self.allMoves = [
            (x*d1,x*d2) for x in range(-7,8)
            for d1 in [-1, 1] for d2 in [-1,1]
        ]
        while (0,0) in self.allMoves:
            self.allMoves.remove((0,0))

    def getLegalMoves(self, board: numpy.ndarray, position: tuple, side: int, ignorePos: tuple):

        moves = self.getLegalMovesByBoard(board, position, side)

        moves = filterDiagonally(board, moves, position, side)

        return [
            (position[0]+x, position[1]+y) for x,y in moves
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

    def getLegalMoves(self, board: numpy.ndarray, position: tuple, side: int, ignorePos: tuple):

        moves = self.getLegalMovesByBoard(board, position, side)

        moves = filterStraight(board, moves, position, side)

        return [
            (position[0]+x, position[1]+y) for x,y in moves
        ]

def filterDiagonally(board: numpy.ndarray, moves, position: tuple, side):
    for d1 in [-1,1]:
            for d2 in [-1,1]:
                blocked = False
                for x in range(0,8):
                    if (x*d1,x*d2) in moves:
                        if blocked == True:
                            moves.remove((x*d1,x*d2))
                            continue

                        if board[position[0]+x*d1, position[1]*x*d2, side] != 0:
                            moves.remove((x*d1,x*d2))
                            blocked = True

                        if board[position[0]+x*d1, position[1]*x*d2, 0 if side==1 else 1] != 0:
                            blocked = True

def filterStraight(board: numpy.ndarray, moves, position: tuple, side):
    blockedX = False
    blockedY = False
    for xOry in range(-7,8):
        if (xOry,0) in moves:
            if blockedX == True:
                moves.remove((0,xOry))
                continue

            if board[position[0]+xOry, position[1], side] != 0:
                moves.remove(((xOry,0)))
                blockedX = True

            if board[position[0]+xOry, position[1], 0 if side==1 else 1] != 0:
                blockedX = True

        if (0,xOry) in moves:
            if blockedY == True:
                moves.remove((0,xOry))
                continue

            if board[position[0], position[1]+xOry, side] != 0:
                moves.remove(((0,xOry)))
                blockedY = True

            if board[position[0], position[1]+xOry, 0 if side==1 else 1] != 0:
                blockedY = True



PIECES_ID_TO_CLASS = {
    10: King(),
    1: Pawn(),
    3: Knight(),
    4: Bishop(),
    5: Rook(),
    9: Queen()
}

PIECES_CLASS_TO_ID = {
    "King": 10,
    "Pawn": 1,
    "Knight": 3,
    "Bishop": 4,
    "Rook": 5,
    "Queen": 9 
}

PIECES_STR_TO_ID = {
    "k": 10,
    "p": 1,
    "n": 3,
    "b": 4,
    "r": 5,
    "q": 9
}

PIECES_ID_TO_STR = {v: k for k, v in PIECES_STR_TO_ID.items()}