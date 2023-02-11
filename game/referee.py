from game.board import *
from game.pieces import *
from game.player import *
from game.move import *

class Referee():

    def __init__(self):
        self.winner = None
        pass
    
    def isValidMove(self, board: numpy.ndarray, position: tuple, move: Move, piecesPos: dict, pieceNum: int, lastMove: Move):
        if move.p == 1:
            legalMoves = PIECES_ID_TO_CLASS(move.p).getLegalMoves(board, position, move.side, piecesPos, move.p, pieceNum, lastMove)
        else:
            legalMoves = PIECES_ID_TO_CLASS(move.p).getLegalMoves(board, position, move.side, piecesPos, move.p, pieceNum)

        if legalMoves == []:
            self.winner = "black" if move.side == "white" else "white"

        return (position[0]+move.x, position[1]+move.y) in legalMoves

    def checkForEnd(self, board: ChessBoard):
        return self.winner != None

    def getWinner(self):
        return self.winner