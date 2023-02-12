from game.board import *
from game.pieces import *
from game.player import *
from game.move import *

class Referee():

    def __init__(self):
        self.winner = None
        self.allLegalMovesLastRound = {}
        pass

    def computeAllLegalMoves(self, board: numpy.ndarray, side: int, piecesPos: dict, lastMove: Move):
        allLegalMoves = {}
        for pieceId in piecesPos[side]:
            for pieceIndex, piecePos in enumerate(piecesPos[side][pieceId]):
                if pieceId == PAWN:
                    allLegalMoves[(pieceId, pieceIndex)] = PIECES_ID_TO_CLASS(pieceId).getLegalMoves(board, tuple(piecePos), side, piecesPos, pieceIndex, pieceIndex, lastMove)
                else:
                    allLegalMoves[(pieceId, pieceIndex)] = PIECES_ID_TO_CLASS(pieceId).getLegalMoves(board, tuple(piecePos), side, piecesPos, pieceIndex, pieceIndex)

        if sum(sum(pieceMoves) for pieceMoves in allLegalMoves.values()):
            self.winner = "black" if side == "white" else "white"


    def isValidMove(self, position: tuple, move: Move, pieceNum: int):

        legalMovesOfPiece = self.allLegalMoves.get((move.p, pieceNum), [])
 
        return (position[0]+move.y, position[1]+move.x) in legalMovesOfPiece

    def isMatchFinished(self):
        return self.winner != None

    def getWinner(self):
        return self.winner