from pieces import *
from move import *
from pieces import Pawn
from typing import Tuple
import numpy



class ChessBoard():
    """"
    Chess board where all positions are stored
    side is the respective player side (white = 1, black = 0)
    """

    def __init__(self):
        "initialize board"

        self.board = numpy.zeros_like((8,8,2), dtype=numpy.byte)

        # 0 = white = on the top half
        # 1 = black = on the bottom half
        # will be switched upside down when viewing because x=0 is at the bottom in chess

        # pawn row
        self.board[1, :, 0] = 1

        # rooks
        self.board[0, 7, 0] = 5
        self.board[0, 0, 0] = 5

        # knights
        self.board[0, 6, 0] = 3
        self.board[0, 1, 0] = 3

        # bishops
        self.board[0, 5, 0] = 4
        self.board[0, 2, 0] = 4

        # queens
        self.board[0, 3, 0] = 9

        # kings
        self.board[0, 4, 0] = 10


        # pawn row
        self.board[6, :, 1] = 1

        # rooks
        self.board[7, 7, 0] = 5
        self.board[7, 0, 0] = 5

        # knights
        self.board[7, 6, 0] = 3
        self.board[7, 1, 0] = 3

        # bishops
        self.board[7, 5, 0] = 4
        self.board[7, 2, 0] = 4

        # queens
        self.board[7, 3, 0] = 9

        # kings
        self.board[7, 4, 0] = 10

        self.piecesPos = {
            0: {
                10: [[0,0]]
            },
            1: {
                10: [[0,0]]
            }
        }


    def getBoard(self, dim: int = 1):
        "get the board either 1 or 2 dimensional"

        assert dim in (1,2)

        # to implement

    
    def makeMove(self, piecePos: tuple, move: Move):
        "move piece"

        currentPiecePos = self.piecesPos[move.side][move.p]
        piecesPosIndex = currentPiecePos.index(list(piecePos))

        currentPiecePos[piecesPosIndex][0] += move.x
        currentPiecePos[piecesPosIndex][1] += move.y

        toRemove = None
        for enemyPId, enemyPiecesPos in self.piecesPos[0 if move.side==1 else 1].items():
            for enemyPiecePos in enemyPiecesPos:
                if enemyPiecePos == (
                    currentPiecePos[piecesPosIndex][0],
                    currentPiecePos[piecesPosIndex][1]
                ):
                    toRemove = (enemyPId, enemyPiecesPos.index(enemyPiecePos))
                    break

        if toRemove != None:
            self.piecesPos[0 if move.side==1 else 1][toRemove[0]].pop(toRemove[1])
            self.board[
                currentPiecePos[piecesPosIndex][0],
                currentPiecePos[piecesPosIndex][1],
                0 if move.side==1 else 1
            ] = 0

        return True

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        # to implement

        return str(self.board)
