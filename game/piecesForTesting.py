import numpy as np


from .move import *
from .relations import *
from .boardfuncs import updateBoardInfo

from string import ascii_uppercase


class ChessBoard2():
    """"
    Chess board where all positions are stored
    side is the respective player side (white = 1, black = 0)
    """

    def __init__(self):
        "initialize board"

        self.board = np.zeros((8,8,2), dtype=np.byte)

        # 0 = black = on the bottom half
        # 1 = white = on the top half
        # will be switched upside down when viewing because x=0 is at the bottom in chess

        # pawn row
        self.board[1, :, BLACK] = PAWN

        # rooks
        self.board[0, 7, BLACK] = ROOK
        self.board[0, 0, BLACK] = ROOK

        # knights
        self.board[0, 6, BLACK] = KNIGHT
        self.board[0, 1, BLACK] = KNIGHT

        # bishops
        self.board[0, 5, BLACK] = BISHOP
        self.board[0, 2, BLACK] = BISHOP

        # queens
        self.board[0, 4, BLACK] = QUEEN

        # kings
        self.board[0, 3, BLACK] = KING


        # pawn row
        self.board[6, :, WHITE] = PAWN

        # rooks
        self.board[7, 7, WHITE] = ROOK
        self.board[7, 0, WHITE] = ROOK

        # knights
        self.board[7, 6, WHITE] = KNIGHT
        self.board[7, 1, WHITE] = KNIGHT

        # bishops
        self.board[7, 5, WHITE] = BISHOP
        self.board[7, 2, WHITE] = BISHOP

        # queens
        self.board[7, 4, WHITE] = QUEEN

        # kings
        self.board[7, 3, WHITE] = KING

        self.piecesPos = {
            0: {
                KING: [[0,3]],
                PAWN: [[1,x] for x in range(8)],
                BISHOP: [[0,2], [0,5]],
                ROOK: [[0,0], [0,7]],
                QUEEN: [[0,4]],
                KNIGHT: [[0,1], [0,6]]
            },
            1: {
                KING: [[7,3]],
                PAWN: [[6,x] for x in range(8)],
                BISHOP: [[7,2], [7,5]],
                ROOK: [[7,0], [7,7]],
                QUEEN: [[7,4]],
                KNIGHT: [[7,1], [7,6]]
            }
        }


    def getBoard(self, dim: int = 1):
        "get the board either 1 or 2 dimensional"

        assert dim in (1,2)

        # to implement

    
    def makeMove(self, piecePos: tuple, move: Move):
        "move piece"

        currentPiecePos = self.piecesPos[move.side][move.p]
        piecePosIndex = currentPiecePos.index(list(piecePos))
        previousPosition = currentPiecePos[piecePosIndex]

        self.board[
            currentPiecePos[piecePosIndex][0], currentPiecePos[piecePosIndex][1], move.side
        ] = 0

        currentPiecePos[piecePosIndex][0] += move.y
        currentPiecePos[piecePosIndex][1] += move.x

        piecePos[move.side][move.p][piecePosIndex][0] += move.y
        piecePos[move.side][move.p][piecePosIndex][1] += move.x

        toRemove = None
        for enemyPId, enemyPiecesPos in self.piecesPos[OTHERSIDE(move.side)].items():
            for enemyPiecePos in enemyPiecesPos:
                if enemyPiecePos == currentPiecePos[piecePosIndex]:
                    toRemove = (enemyPId, enemyPiecesPos.index(enemyPiecePos))
                    break

        if toRemove != None:
            self.piecesPos[OTHERSIDE(move.side)][toRemove[0]].pop(toRemove[1])
            self.board[
                currentPiecePos[piecePosIndex][0],
                currentPiecePos[piecePosIndex][1],
                OTHERSIDE(move.side)
            ] = 0

        # castling

        if move.original.lower() == "o-o":
            self.handleCastling(move, 0, 2)
            
        elif move.original.lower() == "o-o-o":
            self.handleCastling(move, 7, 5)

        # promoting
        elif "=" in move.original:
            self.handlePromotion(move, piecePosIndex)

        self.boardInfo["lastMovePos"] = piecePos[move.side][move.p][piecePosIndex]

        rookStartPosY = 0 if move.side==0 else 7

        if move.p == ROOK:
            if previousPosition == self.board[rookStartPosY, 0, move.side] == ROOK:
                self.boardInfo["firstRookMoved"] = True
            elif previousPosition == self.board[rookStartPosY, 7, move.side] == ROOK:
                self.boardInfo["secondRookMoved"] = True

        return True

    def handleCastling(self, move: Move, rookPosBefore: int, rookPosAfter: int):
        primaryPieceRow = 0 if move.side == 0 else 7
        rookIndex = self.piecesPos[move.side][ROOK].index([
            rookPosBefore, primaryPieceRow
        ])

        rookPos = self.piecesPos[move.side][ROOK][rookIndex]
        self.piecesPos[move.side][ROOK][rookIndex] = [primaryPieceRow, rookPosAfter]
        self.board[rookPos[0], rookPos[1], move.side] = 0
        self.board[primaryPieceRow, rookPosAfter, move.side] = ROOK

    def handlePromotion(self, move: Move, piecePosIndex):
        pieceId = PIECES_STR_TO_ID[move.original.split("=")[1].lower()]
        piecePos = self.piecesPos[move.side][PAWN][piecePosIndex]
        self.piecesPos[move.side][PAWN].pop(piecePosIndex)
        self.piecesPos[move.side][pieceId].append(piecePos)
        self.board[piecePos[0], piecePos[1], move.side] = pieceId

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.toString()

    def toString(self, board=None):
        if board is None:
            board = self.board
        rows = []

        for rowindex in range(8):
            # rows.append(f"{8-rowindex}   " + "   ".join(
            rows.append(f"{rowindex}   " + "   ".join(
                str(
                    self.preparePiece(board[rowindex, colindex, 0], 0)
                    if board[rowindex, colindex, 0] != 0 
                    else self.preparePiece(board[rowindex, colindex, 1], 1)
                )
                for colindex in range(8)
                ))
        # rows.append(
        #     "    " + "   ".join([f"{ascii_uppercase[i]}" for i in range(8)])
        # )
        rows.append(
            "    " + "   ".join([f"{i}" for i in range(8)])
        )

        return "\n\n".join(rows)

    def preparePiece(self, pieceId: int, side: int, testPieceId=None):
        if pieceId == 0:
            return Style.DIM + Fore.LIGHTWHITE_EX +  "_"  + Fore.RESET + Style.RESET_ALL
        if pieceId == testPieceId:
            return TEST_COLOR + "T" + Fore.RESET
        return COLOR_SIDE(side) + PIECES_ID_TO_STR[pieceId].upper() + Fore.RESET

    def visualizeLegalMoves(self, pieceId: int, startPos: tuple=(4,4), level: int=2):
        
        newBoard = np.zeros((8,8,2), dtype=np.byte)

        newBoard[startPos[0], startPos[1],0] = pieceId

        newPiecesPos = {
            0: {KING: [], PAWN: [], BISHOP: [], ROOK: [], QUEEN: [], KNIGHT: []},
            1: {KING: [], PAWN: [(3,x) for x in range(0,8)]+[(6,x) for x in range(0,8)], BISHOP: [], ROOK: [], QUEEN: [], KNIGHT: []}
        }

        newBoardInfo = {
            "lastMovePos": (-1, -1),
            "kingMoved": False,
            "firstRookMoved": False,
            "secondRookMoved": False
        }

        newPiecesPos[0][pieceId].append([4,4])

        #### edit board and piecePos
        newBoard[3, :, 1] = 1
        newBoard[6, :, 1] = 1
        # newBoard[5,4,1] = 1
        ####

        legalMoves = PIECES_ID_TO_CLASS[pieceId].getLegalMoves(newBoard, startPos, 0, newPiecesPos, pieceId, 0, newBoardInfo, level)

        for x, y in legalMoves:
            newBoard[x,y,1] = 12

        rows = []

        for rowindex in range(8):
            # rows.append(f"{8-rowindex}   " + "   ".join(
            rows.append(f"{rowindex}   " + "   ".join(
                str(
                    self.preparePiece(newBoard[rowindex, colindex, 0], 0, 12)
                    if newBoard[rowindex, colindex, 0] != 0 
                    else self.preparePiece(newBoard[rowindex, colindex, 1], 1, 12)
                )
                for colindex in range(8)
                ))
        # rows.append(
        #     "    " + "   ".join([f"{ascii_uppercase[i]}" for i in range(8)])
        # )
        rows.append(
            "    " + "   ".join([f"{i}" for i in range(8)])
        )

        print("\n\n".join(rows))

class Figure():
    """
    Chess figure
    moveLen = Number of moves in each moveDirection
    moveDirections = Change in x,y position of the figure, third element = if piece needs to be
    """

    def getLegalMovesByBoard(self, board: np.ndarray, position: tuple, side: int):
        allmoves = self.allMoves.copy()
        allmoves2 = [
            (x,y) for x,y in allmoves if 0 <= position[0]+y < 8 and 0 <= position[1]+x < 8
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

    def getLegalMoves(self, board: np.ndarray, position: tuple, side: int, piecesPos: dict, pieceId: int, pieceIndex: int, boardInfo: dict, level: int=1):

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

        if level<=2: # for tests only
            moves = filterForCheckNextMove(board, moves, position, side, piecesPos, pieceId, pieceIndex, boardInfo, level)

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

        moves = filterStraight(board, moves, position, side, level)
        moves = filterDiagonally(board, moves, position, side, level)

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
                if board[position[0], position[1]-1, OTHERSIDE(side)] == PAWN and boardInfo["lastMovePos"][1] == position[1]-1 and boardInfo["lastMovePos"][0] == position[1]:
                    moves.append((1,sideDir*1))

        if (1,sideDir*1) in moves:
            if board[position[0]+sideDir*1, position[1]+1, OTHERSIDE(side)] == 0:
                moves.remove((1,sideDir*1))
            
                # en passant    
                if board[position[0], position[1]+1, OTHERSIDE(side)] == PAWN and boardInfo["lastMovePos"][1] == position[1]+1 and boardInfo["lastMovePos"][0] == position[1]:
                    moves.append((1,sideDir*1))

        if np.any(board[position[0]+sideDir*1, position[1], OTHERSIDE(side)] != 0):
            moves.remove((0,sideDir*1))

        # if pawn hasnt moved yet: can move 2 pieces
        startPos = 1 if side==0 else 6
        # if pawn hasnt moved yet, space is not occupied, and piece can move 1 further already
        if position[0] == startPos and \
            allIdInBoardRange(board, position[0]+sideDir*2, position[1], (0,1), 0) and \
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

        moves = filterDiagonally(board, moves, position, side, level)

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

        moves = filterStraight(board, moves, position, side, level)

        if level == 1:
            moves = filterForCheckNextMove(board, moves, position, side, piecesPos, pieceId, pieceIndex, boardInfo)

        return [
            (position[0]+y, position[1]+x) for x,y in moves
        ]

def filterDiagonally(board: np.ndarray, moves, position: tuple, side: int, level: int=0):
    if level==2:
        board2 = ChessBoard2()
        board2.visualizeLegalMoves(board[position[0], position[1], side], position, level+1)

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

def filterStraight(board: np.ndarray, moves, position: tuple, side: int, level: int=0):
    if level==2:
        board2 = ChessBoard2()
        board2.visualizeLegalMoves(board[position[0], position[1], side], position, level+1)

    blockedX = False
    blockedY = False
    for xOry in range(-1,-8,-1):
        # y-moves
        if (0,xOry) in moves:
            if blockedX == True:
                moves.remove((0,xOry))
                continue

            if board[position[0]+xOry, position[1], side] != 0:
                moves.remove(((0,xOry)))
                blockedX = True

            if board[position[0]+xOry, position[1], OTHERSIDE(side)] != 0:
                blockedX = True

        # x-moves
        if (xOry,0) in moves:
            if blockedY == True:
                moves.remove((xOry, 0))
                continue

            if board[position[0], position[1]+xOry, side] != 0:
                moves.remove(((xOry, 0)))
                blockedY = True

            if board[position[0], position[1]+xOry, OTHERSIDE(side)] != 0:
                blockedY = True

    blockedX = False
    blockedY = False
    for xOry in range(0,8):
        # y-moves
        if (0,xOry) in moves:
            if blockedX == True:
                moves.remove((0,xOry))
                continue

            if board[position[0]+xOry, position[1], side] != 0:
                moves.remove(((0,xOry)))
                blockedX = True

            if board[position[0]+xOry, position[1], OTHERSIDE(side)] != 0:
                blockedX = True

        # x-moves
        if (xOry,0) in moves:
            if blockedY == True:
                moves.remove((xOry, 0))
                continue

            if board[position[0], position[1]+xOry, side] != 0:
                moves.remove(((xOry, 0)))
                blockedY = True

            if board[position[0], position[1]+xOry, OTHERSIDE(side)] != 0:
                blockedY = True
                
    return moves

def filterForCheckNextMove(board: np.ndarray, moves, position: tuple, side: int, piecesPos: dict, pieceId: int, pieceIndex: int, boardInfo: dict, level: int=1):
    
    position_orig = position
    moves2 = []

    # print("moves")
    # print(moves)
    # print("-------------------")
    allEnemyPieces = [
        (pieceId2, enemypieceIndex)
        for pieceId2, piecelist in piecesPos[OTHERSIDE(side)].items() 
        for enemypieceIndex in range(len(piecelist))
    ]
    for move in moves:
        position = (position_orig[0]+move[1], position_orig[1]+move[0])


        piecesPosCopy = piecesPos.copy()
        # # testing
        # # print("PID 5")
        # # print(piecesPosCopy)
        # # print(side)
        # # print(pieceId)
        # # print(pieceIndex)
        previousPosition = piecesPosCopy[side][pieceId][pieceIndex]
        piecesPosCopy[side][pieceId][pieceIndex] = position

        board2 = board.copy()

        board2[position_orig[0], position_orig[1], side] = 0
        board2[position[0], position[1], side] = pieceId
        board2[position[0], position[1], OTHERSIDE(side)] = 0

        cb = ChessBoard2()
        print(cb.toString(board2))

        boardInfo2 = updateBoardInfo(board2, boardInfo.copy(), side, piecesPos, pieceId, pieceIndex, previousPosition)

        # print(allEnemyPieces)
        canTakeThisMove = True
        for pieceId2, enemypieceIndex in allEnemyPieces:
            # print(pieceId)
            # print(enemypieceIndex)
            enemyPieceMoves = PIECES_ID_TO_CLASS[pieceId2].getLegalMoves(board2, tuple(piecesPosCopy[OTHERSIDE(side)][pieceId2][enemypieceIndex]), OTHERSIDE(side), piecesPosCopy, pieceId2, enemypieceIndex, boardInfo2, level=level+1)

            if piecesPosCopy[side][KING][0] in enemyPieceMoves:
                canTakeThisMove = False
        
        if canTakeThisMove:
            moves2.append(move)
            # print("----")
        print("---------")


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