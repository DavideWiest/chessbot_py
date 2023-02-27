from game.board import *
from game.pieces import *
from game.player import *
from game.move import *
from game.referee import *

import copy

class moveSimulator():
    def __init__(self, board: ChessBoard, referee: Referee, side: int, legalMovesPositions, depth=3):
        self.board = copy.deepcopy(board)
        self.referee = referee
        self.nestedMoves = {}
        self.side = side

        self.bestMoveScore = float("inf")
        self.lastMove = None

        # getMoveNodes of the deepest move nodes with alternating side
        for pid in legalMovesPositions:
            for moveYX in legalMovesPositions:
                dph = 0
                # save infos to roll back
                pieceAtYX = self.board[moveYX[0], moveYX[1], OTHERSIDE(side)]
                self.nestedMoves[(pid, moveYX[0], moveYX[1])] = self.getMoveNodes()
                # roll back board

    def getMoveNodes(self):
        "get legal or expected next move (1)"

        self.referee.winner = None
        self.referee.allLegalMoves = {}
        self.referee.computeAllLegalMoves()
        return self.referee.allLegalMoves

    def bestMoveGenerator(self):
        "yield best move, yield best move thats lower than self.bestMoveScore, then update it accordingly, returns list of Move"

    def evalDeepest(self):
        pass

class AlgoPlayer(Player):

    def __init__(self, side: int, color: str):
        self.side = side
        self.color = color
        self.needsValidityChecked = False
        self.needsAllLegalMoves = True

        self.referee = Referee()

    def getMove(self, gh, legalMovesPositions: tuple):
        ms = moveSimulator(gh.board, self.referee, self.side, legalMovesPositions)
        
        for move in ms.bestMoveGenerator():
            if self.validateMove(self, move):
                return move

    def validateMove(self, move):
        return True

    def wait(self):
        pass

