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
        self.depth = depth

        self.bestMoveScore = float("inf")
        self.lastMove = None

        # begin loop
        self.nestedMoves = self.iterLegalMoves(legalMovesPositions)

    def iterLegalMoves(self, legalMovesPositions, currentSide, depth=0):
        # getMoveNodes of the deepest move nodes with alternating side
        nestedNextMoves = {}
        for pId in legalMovesPositions:
            for i, moveYX in legalMovesPositions[pId].items():
                piecePos = self.board.piecePos[currentSide][pId][i]
                nestedNextMoves[(pId, moveYX[0], moveYX[1])] = self.simulateMove(pId, moveYX, piecePos, currentSide, depth)
        return nestedNextMoves
    
    def simulateMove(self, pId, moveYX, piecePos, currentSide, depth=0):
        # save infos to roll back
        boardBefore = self.board.board.copy()
        piecesPosBefore = copy.deepcopy(self.board.piecesPos)
        gameState = copy.deepcopy(self.board.boardInfo)
        move = MoveWithInts(pId, moveYX[1], moveYX[0], currentSide, piecePos)
        self.board.makeMove(move)
        legalMovesPositions = self.getLegalMoves()
        if len(self.board.piecePos[OTHERSIDE(currentSide)][KING]) == 0:
            self.referee.setWinner(OTHERSIDE(currentSide))
        if self.referee.winner != None:
            if self.referee.winner == self.side:
                return 1
            else:
                return -1
            
        if depth >= self.depth:
            self.evalDeepest(legalMovesPositions)
        else:
            return self.iterLegalMoves(legalMovesPositions, OTHERSIDE(currentSide), depth+1)
        
        # roll back board
        self.board.board = boardBefore
        self.board.piecesPos = piecesPosBefore
        self.boardInfo = gameState

    def getLegalMoves(self, currentSide):
        "get legal or expected next move (1)"

        self.referee.winner = None
        self.referee.allLegalMoves = {}
        self.referee.computeAllLegalMoves(self.board, currentSide)
        return self.referee.allLegalMoves

    def bestMoveGenerator(self):
        "yield best move, yield best move thats lower than self.bestMoveScore, then update it accordingly, returns list of Move"

        # recursively find mean strength, starting from the deepest

    def evalDeepest(self, legalMovesPositions):
        "evaluate player strength compared to enemy player strength, and normalize into a value from -1 to 1"
        k = 0.001

        # iterate over board, use legal moves

        # use meanTilesThreatening[pId]

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

