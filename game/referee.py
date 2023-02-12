from game.board import *
from game.pieces import *
from game.player import *
from game.move import *

class Referee():

    def __init__(self):
        self.winner = None
        self.allLegalMoves = {}
        pass

    def computeAllLegalMoves(self, board: numpy.ndarray, side: int, piecesPos: dict, lastMove: Move):
        self.allLegalMoves = {}
        for pieceId in piecesPos[side]:
            # testing
            # print("PID")
            # print(pieceId)
            for pieceIndex, piecePos in enumerate(piecesPos[side][pieceId]):
                # print("PIN")
                # print(pieceIndex)
                if pieceId == PAWN:
                    self.allLegalMoves[(pieceId, pieceIndex)] = PIECES_ID_TO_CLASS[pieceId].getLegalMoves(board, tuple(piecePos), side, piecesPos, pieceId, pieceIndex, lastMove)
                else:
                    self.allLegalMoves[(pieceId, pieceIndex)] = PIECES_ID_TO_CLASS[pieceId].getLegalMoves(board, tuple(piecePos), side, piecesPos, pieceId, pieceIndex)

        if sum(len(pieceMoves) for pieceMoves in self.allLegalMoves.values()):
            self.winner = "black" if side == "white" else "white"


    def isValidMove(self, position: tuple, move: Move, pieceIndex: int):

        legalMovesOfPiece = self.allLegalMoves.get((move.p, pieceIndex), [])
 
        return (position[0]+move.y, position[1]+move.x) in legalMovesOfPiece

    def isMatchFinished(self):
        return self.winner != None

    def getWinner(self):
        return self.winner