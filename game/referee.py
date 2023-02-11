from game.board import *
from game.pieces import *
from game.player import *
from game.move import *

class Referee():

    def __init__(self):
        self.winner = None
        pass
    
    def isValidMove(self, board: numpy.ndarray, position: tuple, move: Move, makeValidation: bool = True):
        if makeValidation:
            # to implement

            if move.p == 10:
                PIECES_ID_TO_CLASS(move.p).getLegalMoves()

            return

        return True

    def checkForEnd(self, board: ChessBoard):
        # to implement
        
        self.winner = ""

        return False

    def getWinner(self):
        return self.winner