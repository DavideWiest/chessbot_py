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

        # pawn rows
        self.board[1, :, 0] = 1
        self.board[6, :, 1] = 1

        # to implement
        # rooks
        self.board[0, 8]

        # bishops


        # knights


        # queens


        # kings


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
