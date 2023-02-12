from .pieces import *
from .move import *
import numpy

from colorama import Fore, Back, Style


class ChessBoard():
    """"
    Chess board where all positions are stored
    side is the respective player side (white = 1, black = 0)
    """

    def __init__(self):
        "initialize board"

        self.board = numpy.zeros((8,8,2), dtype=numpy.byte)

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
                KNIGHT: [[0,1], [0,6]],
                BISHOP: [[0,2], [0,5]],
                ROOK: [[0,0], [0,7]],
                QUEEN: [[0,4]]
            },
            1: {
                KING: [[7,3]],
                PAWN: [[6,x] for x in range(8)],
                KNIGHT: [[7,1], [7,6]],
                BISHOP: [[7,2], [7,5]],
                ROOK: [[7,0], [7,7]],
                QUEEN: [[7,4]]
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

        self.board[
            currentPiecePos[piecePosIndex][0], currentPiecePos[piecePosIndex][1], move.side
        ] = 0

        currentPiecePos[piecePosIndex][0] += move.y
        currentPiecePos[piecePosIndex][1] += move.x

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
        # to implement

        rows = []

        for rowindex in range(7):
            rows.append(" ".join(
                str(
                    self.board[rowindex][colindex][0] 
                    if self.board[rowindex][colindex][0] != 0 
                    else self.board[rowindex][colindex][1]
                )
                for colindex in range(7)
                ))

        return "\n\n".join(rows)

    def preparePiece(pieceId: int, side: int):
        return (
            Fore.GREEN + PIECES_ID_TO_STR(pieceId).upper() + Fore.RESET 
            if side == 0 
            else Fore.WHITE + PIECES_ID_TO_STR(pieceId).upper() + Fore.RESET
        )
