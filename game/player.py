from board import ChessBoard

class Player():

    def __init__(self):
        raise NotImplementedError

    def getMove(self, board: ChessBoard):
        raise NotImplementedError