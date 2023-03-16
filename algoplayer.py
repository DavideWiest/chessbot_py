from game.board import *
from game.pieces import *
from game.player import *
from game.move import *
from game.referee import *

import copy
import json
from statistics import median

DEPTH = 3

class moveSimulator():
    def __init__(self, board: ChessBoard, referee: Referee, side: int, legalMovesPositions, depth=DEPTH):
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
                nestedNextMoves[(pId, i, moveYX[0], moveYX[1])] = self.simulateMove(pId, moveYX, piecePos, currentSide, depth)
        return nestedNextMoves
    
    def simulateMove(self, pId, moveYX, piecePos, currentSide, depth=0):
        # save infos to roll back
        boardBefore = self.board.board.copy()
        piecesPosBefore = copy.deepcopy(self.board.piecesPos)
        gameState = copy.deepcopy(self.board.boardInfo)
        move = MoveWithInts(pId, moveYX[1], moveYX[0], currentSide, piecePos)
        self.board.makeMove(move)
        legalMovesPositions = self.getLegalMoves(currentSide)

        if len(self.board.piecePos[OTHERSIDE(currentSide)][KING]) == 0:
            self.referee.setWinner(OTHERSIDE(currentSide))
        if self.referee.winner != None:
            if self.referee.winner == self.side:
                return 1
            else:
                return -1
            
        if depth >= self.depth:
            enemyLegalMovesPos = self.getLegalMoves(OTHERSIDE(currentSide))
            cbe = ChessBoardEvaluator(self.board, self.referee, legalMovesPositions, enemyLegalMovesPos, self.board.piecesPos, self.side)
            return cbe.evalDeepest()
        else:
            # roll back board
            self.board.board = boardBefore
            self.board.piecesPos = piecesPosBefore
            self.boardInfo = gameState
            return self.iterLegalMoves(legalMovesPositions, OTHERSIDE(currentSide), depth+1)
        

    def getLegalMoves(self, currentSide):
        "get legal or expected next move (1)"

        self.referee.winner = None
        self.referee.allLegalMoves = {}
        self.referee.computeAllLegalMoves(self.board, currentSide)
        return self.referee.allLegalMoves
    
    def simplifyToSingleNum(self, branch):
        if isinstance(branch, int) or isinstance(branch, float): return branch
        return median(self.simplifyToSingleNum(branch2) for branch2 in branch)
    
    def bestMoveGenerator(self):
        "yield best move, yield best move thats lower than self.bestMoveScore, then update it accordingly, returns list of Move"

        # recursively find mean strength, starting from the deepest
        movesByValue = {k: self.simplifyToSingleNum(branch) for k,branch in self.nestedMoves.items()}
        movesByValue = {k: v for k, v in sorted(movesByValue.items(), key=lambda item: item[1])}

        for pId, pIndex, Y, X in movesByValue.keys():
            move = MoveWithInts(pId, X, Y, self.side, tuple(self.board.piecesPos[self.side][pId][pIndex]))
            yield move

class ChessBoardEvaluator():
    def __init__(self, board: ChessBoard, referee: Referee, legalMovesPos, enemyLegalMovesPos, piecesPos, side):
        self.board = board
        self.referee = referee
        self.lmp = legalMovesPos
        self.elmp = enemyLegalMovesPos
        self.piecesPos = piecesPos
        self.side = side
        # to prevent zerodivisionerror
        self.k = 0.00001
        # maximal multiplication of a piece value when calculating threatened and protected by
        self.maxMul = 5
        # used to bring factor closer to 1, reducing its weight 
        self.nthSquareRoot = 1/3.5
        # pure value of threats, even if enemy piece is protected by lower value piece
        self.pieceK = 0.5

        with open("data/meanTilesThreatening.json", "r") as f:
            self.meanTilesThreatening = {int(pId): v for pId, v in json.load(f).items()}
        
        self.maxPieceValue = max(self.meanTilesThreatening.values())
    
    def evalDeepest(self):
        "evaluate player strength compared to enemy player strength, and normalize into a value from -1 to 1"
        pStrength = 0
        eStrength = 0

        for pId in self.piecesPos[self.side]:
            for pIndex in range(len(self.piecesPos[self.side])):
                # pos = tuple(self.piecesPos[self.side][pId][pIndex])
                legalMoves = self.lmp[pId][pIndex]
                pStrength += self._getPieceValue(pId) \
                    * (self._getTilesThreatening(legalMoves, self.side) \
                    / self._getMeanTilesThreatening(pId)) ** (1/self.nthSquareRoot) \
                    * self._getThreatenedAndProtectedBy(self.side, pId, pIndex)
        
        for pId in self.piecesPos[OTHERSIDE(self.side)]:
            for pIndex in range(len(self.piecesPos[OTHERSIDE(self.side)])):
                # pos = tuple(self.piecesPos[OTHERSIDE(self.side)][pId][pIndex])
                legalMoves = self.lmp[pId][pIndex]
                eStrength += self._getPieceValue(pId) \
                    * (self._getTilesThreatening(legalMoves, OTHERSIDE(self.side)) \
                    / self._getMeanTilesThreatening(pId)) ** (1/self.nthSquareRoot) \
                    * self._getThreatenedAndProtectedBy(OTHERSIDE(self.side), pId, pIndex)
                
        return pStrength / ((pStrength + eStrength) / 2) - 1

    def _getPieceValue(self, pId):
        # if pId == 0: return 0.2
        if pId == 4: return 3.5
        return pId

    def _getTilesThreatening(self, legalMoves, currentSide):
        return len(move for move in legalMoves if self.board.board[move[0], move[1], OTHERSIDE(currentSide)] == 0)
    
    def _getTilesThreateningByPieceId(self, legalMoves, pId, currentSide):
        return len(move for move in legalMoves[pId] if self.board.board[move[0], move[1], OTHERSIDE(currentSide)] == 0)

    def _getMeanTilesThreatening(self, pId):
        return self.meanTilesThreatening[pId]
    
    def _getThreatenedAndProtectedBy(self, currentSide, pId, pIndex, returnValueForStrengthCalc=True):
        # delete piece
        # get legal moves and check how often it is inside the legal moves list of a piece
        # if checkmate: return k

        threatenedBy = self.k
        protectedBy = 0

        pos = tuple(self.piecesPos[currentSide][pId][pIndex])
        del self.piecesPos[currentSide][pId][pIndex]
        self.board[pos[0], pos[1], currentSide] = 0

        legalMoves1 = self.referee.computeAllLegalMoves(self.board, currentSide)
        legalMoves2 = self.referee.computeAllLegalMoves(self.board, OTHERSIDE(currentSide))

        for pId2 in legalMoves1:
            for pIndex2 in legalMoves1[pId2]:
                if legalMoves1[pId2][pIndex2] == pos:
                    protectedBy += (self.maxPieceValue - self._getPieceValue(pId2) + self.pieceK)

        for pId2 in legalMoves2:
            for pIndex2 in legalMoves2[pId2]:
                if legalMoves1[pId2][pIndex2] == pos:
                    threatenedBy += (self.maxPieceValue - self._getPieceValue(pId2) + self.pieceK)

        if returnValueForStrengthCalc:
            return min(protectedBy / threatenedBy, self.maxMul)
        else:
            return threatenedBy, protectedBy

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

