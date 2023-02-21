import numpy as np

from .move import *
from .relations import *
from .boardfuncs import updateBoardInfo

class Figure():
    """
    Chess figure
    moveLen = Number of moves in each moveDirection
    moveDirections = Change in x,y position of the figure, third element = if piece needs to be
    """

    def getLegalMovesByBoard(self, board: np.ndarray, position: tuple, side: int, directionMul=1):
        allmoves = self.allMoves.copy()
        if directionMul != 1:
            allmoves = [(x,directionMul*y) for x,y in allmoves]
        allmoves2 = [
            (x,y) for x,y in allmoves if 0 <= position[0]+y < 8 and 0 <= position[1]+x < 8
        ]

        moves = [
            (x,y) for x,y in allmoves2 if board[position[0]+y, position[1]+x, side] == 0
        ]

        return moves

    def __repr__(self):
        return PIECES_ID_TO_STR[PIECES_NAME_TO_ID[self.__class__.__name__]]

class King(Figure):
    def __init__(self):
        self.allMoves = [
            (x,y) for x in range(-1,2) for y in range(-1,2)
        ]
        while (0,0) in self.allMoves:
            self.allMoves.remove((0,0))

    def getLegalMoves(self, board: np.ndarray, position: tuple, side: int, piecesPos: dict, pieceId: int, pieceIndex: int, boardInfo: dict, level: int=1):

        # to implement

        moves = self.getLegalMovesByBoard(board, position, side)

        # castling
        startPos = (0 if side==0 else 7, 3)

        # if king and rook in startposition, and none of the spaces in between are occupied
        if position == startPos and \
            boardInfo[side]["kingMoved"] == False and \
            boardInfo[side]["firstRookMoved"] == False and \
            board[startPos[0], 0, side] == ROOK and \
            allIdInBoardRange(board, startPos[0], (1,3), (0,1), 0):
            moves.append((startPos[0], 1))
        
        if position == startPos and \
            boardInfo[side]["kingMoved"] == False and \
            boardInfo[side]["secondRookMoved"] == False and \
            board[startPos[0], 7, side] == ROOK and \
            allIdInBoardRange(board, startPos[0], (4,7), (0,1), 0):
            moves.append((startPos[0], 6))

        if level == 1:
            moves = filterForCheckNextMove(board, moves, position, side, piecesPos, pieceId, pieceIndex, boardInfo)

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

    def getLegalMoves(self, board: np.ndarray, position: tuple, side: int, piecesPos: dict, pieceId: int, pieceIndex: int, boardInfo: dict, level: int=1):

        moves = self.getLegalMovesByBoard(board, position, side)

        # sort out moves that are blocked
        
        if level==1:
            print("QUEEN MOVES")
            print(moves)
        moves = filterStraight(board, moves, position, side)
        if level==1:
            print("QUEEN MOVES")
            print(moves)
        moves = filterDiagonally(board, moves, position, side)
        if level==1:
            print("QUEEN MOVES")
            print(moves)

        if level == 1:
            moves = filterForCheckNextMove(board, moves, position, side, piecesPos, pieceId, pieceIndex, boardInfo)

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

    def getLegalMoves(self, board: np.ndarray, position: tuple, side: int, piecesPos: dict, pieceId: int, pieceIndex: int, boardInfo: dict, level: int=1):

        sideDir = DIRECTION(side)
        moves = self.getLegalMovesByBoard(board, position, side, sideDir)

        # pawns can only move downwards if side == white else only upwards
        if (-1,sideDir*1) in moves:
            if board[position[0]+sideDir*1, position[1]-1, OTHERSIDE(side)] == 0:
                moves.remove((-1,sideDir*1))

                # en passant
                if board[position[0], position[1]-1, OTHERSIDE(side)] == PAWN and boardInfo[side]["lastMovePos"][1] == position[1]-1 and boardInfo[side]["lastMovePos"][0] == position[0]:
                    moves.append((-1,sideDir*1))

        if (1,sideDir*1) in moves:
            # an indexerror occured here: position[1]+1 was 8
            if board[position[0]+sideDir*1, position[1]+1, OTHERSIDE(side)] == 0:
                moves.remove((1,sideDir*1))
            
                # en passant    
                if board[position[0], position[1]+1, OTHERSIDE(side)] == PAWN and boardInfo[side]["lastMovePos"][1] == position[1]+1 and boardInfo[side]["lastMovePos"][0] == position[0]:
                    moves.append((1,sideDir*1))

        if (0,sideDir*1) in moves:
            if np.any(board[position[0]+sideDir*1, position[1], :] != 0):
                moves.remove((0,sideDir*1))

        # if pawn hasnt moved yet: can move 2 pieces
        startPos = 1 if side==0 else 6
        # if pawn hasnt moved yet, space is not occupied, and piece can move 1 further already
        if position[0] == startPos:
            if np.all(board[position[0]+sideDir*2, position[1], :] == 0) and \
            (0,sideDir*1) in moves:
                moves.append((0, sideDir*2))

        if level == 1:
            moves = filterForCheckNextMove(board, moves, position, side, piecesPos, pieceId, pieceIndex, boardInfo)

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

    def getLegalMoves(self, board: np.ndarray, position: tuple, side: int, piecesPos: dict, pieceId: int, pieceIndex: int, boardInfo: dict, level: int=1):

        moves = self.getLegalMovesByBoard(board, position, side)

        if level == 1:
            moves = filterForCheckNextMove(board, moves, position, side, piecesPos, pieceId, pieceIndex, boardInfo)

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

    def getLegalMoves(self, board: np.ndarray, position: tuple, side: int, piecesPos: dict, pieceId: int, pieceIndex: int, boardInfo: dict, level: int=1):

        moves = self.getLegalMovesByBoard(board, position, side)

        moves = filterDiagonally(board, moves, position, side)

        if level == 1:
            moves = filterForCheckNextMove(board, moves, position, side, piecesPos, pieceId, pieceIndex, boardInfo)

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

    def getLegalMoves(self, board: np.ndarray, position: tuple, side: int, piecesPos: dict, pieceId: int, pieceIndex: int, boardInfo: dict, level: int=1):

        moves = self.getLegalMovesByBoard(board, position, side)

        moves = filterStraight(board, moves, position, side)

        if level == 1:
            moves = filterForCheckNextMove(board, moves, position, side, piecesPos, pieceId, pieceIndex, boardInfo)

        return [
            (position[0]+y, position[1]+x) for x,y in moves
        ]

def filterDiagonally(board: np.ndarray, moves, position: tuple, side: int):
    for dX in [-1,1]:
            for dY in [-1,1]:
                blocked = False
                for x in range(1,8):
                    if blocked == True:
                        if (x*dX,x*dY) in moves:
                            moves.remove((x*dX,x*dY))
                        continue

                    # avoid indexerror
                    # if (x,x) in any diagonal direction have already been blocked, it was because of the board
                    # if we would check again with the board, itd yield an indexerror
                    # switched because moves is x,y but board is accessed with y,x
                    if (x*dX, x*dY) not in moves:
                        blocked = True
                        continue

                    if board[position[0]+x*dY, position[1]+x*dX, side] != 0:
                        if (x*dX,x*dY) in moves:
                            moves.remove((x*dX,x*dY))
                        blocked = True

                    if board[position[0]+x*dY, position[1]+x*dX, OTHERSIDE(side)] != 0:
                        blocked = True

    return moves

def filterStraight(board: np.ndarray, moves, position: tuple, side: int):

    for dir in [-1,1]:
        blockedY = False
        blockedX = False

        for xOry in range(1,8):
            # y-moves
            
            if blockedY == True:
                if (0,dir*xOry) in moves:
                    moves.remove((0,dir*xOry))
            # avoid indexerror
            elif position[0]+dir*xOry > 7 or position[0]+dir*xOry < 0:
                blockedY = True
            else:

                if board[position[0]+dir*xOry, position[1], side] != 0:
                    if (0,dir*xOry) in moves:
                        moves.remove((0,xOry))
                    blockedY = True

                if board[position[0]+dir*xOry, position[1], OTHERSIDE(side)] != 0:
                    blockedY = True

            # x-moves
            
            if blockedX == True:
                if (dir*xOry, 0) in moves:
                    moves.remove((dir*xOry, 0))
            # avoid indexerror
            elif position[1]+dir*xOry > 7 or position[1]+dir*xOry < 0:
                blockedX = True
            else:

                if board[position[0], position[1]+dir*xOry, side] != 0:
                    if (dir*xOry, 0) in moves:
                        moves.remove((dir*xOry, 0))
                    blockedX = True

                if board[position[0], position[1]+dir*xOry, OTHERSIDE(side)] != 0:
                    blockedX = True
                        
    return moves

def filterForCheckNextMove(board: np.ndarray, moves, position: tuple, side: int, piecesPos: dict, pieceId: int, pieceIndex: int, boardInfo: dict):
    
    position_orig = position
    moves2 = []

    allEnemyPieces = [
        (pieceId2, enemypieceIndex)
        for pieceId2, piecelist in piecesPos[OTHERSIDE(side)].items() 
        for enemypieceIndex in range(len(piecelist))
    ]
    for move in moves:
        position = (position_orig[0]+move[1], position_orig[1]+move[0])


        piecesPosCopy = {
            0: {
                pId: pMoves.copy() for pId, pMoves in piecesPos[0].items()
            },
            1: {
                pId: pMoves.copy() for pId, pMoves in piecesPos[1].items()
            }
        }

        previousPosition = piecesPosCopy[side][pieceId][pieceIndex]
        piecesPosCopy[side][pieceId][pieceIndex] = position

        board2 = board.copy()

        board2[position_orig[0], position_orig[1], side] = 0
        board2[position[0], position[1], side] = pieceId
        board2[position[0], position[1], OTHERSIDE(side)] = 0

        boardInfo2 = {}
        boardInfo2[0], boardInfo2[1] = boardInfo[0].copy(), boardInfo[1].copy()
        boardInfo2[side] = updateBoardInfo(board2, boardInfo2[side], piecesPosCopy, side, pieceId, pieceIndex, previousPosition)

        if pieceId == QUEEN:
            print("QUEEN")
            print(move)

        canTakeThisMove = True
        positionsToCheckLater = []
        combinedEnemyMoves = []
        for pieceId2, enemypieceIndex in allEnemyPieces:
            enemyPosition = tuple(piecesPosCopy[OTHERSIDE(side)][pieceId2][enemypieceIndex])
            enemyPieceMoves = PIECES_ID_TO_CLASS[pieceId2].getLegalMoves(board2, enemyPosition, OTHERSIDE(side), piecesPosCopy, pieceId2, enemypieceIndex, boardInfo2, level=2)
            combinedEnemyMoves += enemyPieceMoves
                
            if tuple(piecesPosCopy[side][KING][0]) in enemyPieceMoves:
                print("checking vicinity of")
                print(PIECES_ID_TO_NAME[pieceId2])
                print(tuple(piecesPosCopy[side][KING][0]))
                print(tuple(piecesPosCopy[side][KING][0]) in vicinityOf(enemyPosition, 1))
                if tuple(piecesPosCopy[side][KING][0]) in vicinityOf(enemyPosition, 1):
                    positionsToCheckLater.append(enemyPosition)
                else:
                    canTakeThisMove = False
                    break
        
        # check if king could take the piece that checks it
        print("check if king could take the piece")
        print([pos in combinedEnemyMoves for pos in positionsToCheckLater])
        print(any(pos in combinedEnemyMoves for pos in positionsToCheckLater))
        if any(pos in combinedEnemyMoves for pos in positionsToCheckLater):
            canTakeThisMove = False
        
        if canTakeThisMove:
            moves2.append(move)

    return moves2


def allIdInBoardRange(board: np.ndarray, yRange, xRange, sideOneOrBoth, wantedId=0):
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

def vicinityOf(position: tuple, stepsY: int, stepsX: int=None):
    "as tuples"
    
    if stepsX == None:
        stepsX = stepsY
    return [
        (position[0]+stepY, position[1]+stepX)
        for stepY in range(-stepsY, stepsY+1)
        for stepX in range(-stepsX, stepsX+1)
    ]

PIECES_ID_TO_CLASS = {
    KING: King(),
    PAWN: Pawn(),
    KNIGHT: Knight(),
    BISHOP: Bishop(),
    ROOK: Rook(),
    QUEEN: Queen()
}
