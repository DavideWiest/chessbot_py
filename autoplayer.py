from game.player import Player
from game.move import *
from game.relations import PIECES_ID_TO_STR
from algoplayer import ChessBoardAnalyzer
from datamanipulation import getAvgOf2Dicts, getAvgOf2DList
import traceback

DATA_PIECES_AT_INDEX = [
    "tilesThreateningByPieceP0",
    "tilesThreateningByPieceP1",
    "threatenedbyByPieceP0",
    "threatenedbyByPieceP1",
    "protectedbyByPieceP0",
    "protectedbyByPieceP1"
]

class AutoPlayer(Player):
    def __init__(self, moves, side, analyzeBoard=True):
        self.needsAllLegalMoves = True
        self.needsValidityChecked = False
        self.moves = moves
        self.side = side
        self.analyzeBoard = analyzeBoard
        self.keys = DATA_PIECES_AT_INDEX
        self.numBoardAnalyses = 0
        self.data = [
            {} for _ in range(len(self.keys))
        ]

    def doBoardAnalysis(self, gh, legalMovesPositions):
        lmpDict = {
            self.side: legalMovesPositions,
            OTHERSIDE(self.side): gh.referee.computeAllLegalMoves(gh.board, OTHERSIDE(self.side), True)
        }
        cbe = ChessBoardAnalyzer(gh.board, gh.referee, legalMovesPositions, lmpDict[OTHERSIDE(self.side)], gh.board.piecesPos, self.side)

        # temporarily storing it in a variable because the 2 return values will be saved separately
        numPiecesExistingP0 = {pId: len(lmpDict[0][pId]) for pId in PIECES_ID_TO_STR}
        threatenedAndProtectedByP0 = {
            pId: getAvgOf2DList(cbe._getThreatenedAndProtectedBy(0, pId, i, False))
            for pId in PIECES_ID_TO_STR
            for i in range(numPiecesExistingP0[pId])
        }
        threatenedAndProtectedByP1 = {
            pId: getAvgOf2DList(cbe._getThreatenedAndProtectedBy(1, pId, i, False))
            for pId in PIECES_ID_TO_STR
            for i in range(numPiecesExistingP0[pId])
        }

        self.data = [
            getAvgOf2Dicts(
                self.data[0],
                {pId: cbe._getMeanTilesThreateningByPieceId(lmpDict[0], pId, 0) for pId in PIECES_ID_TO_STR},
                self.numBoardAnalyses
            ),
            getAvgOf2Dicts(
                self.data[1],
                {pId: cbe._getMeanTilesThreateningByPieceId(lmpDict[1], pId, 1) for pId in PIECES_ID_TO_STR},
                self.numBoardAnalyses
            ),
            getAvgOf2Dicts(
                self.data[2],
                {pId: threatenedAndProtectedByP0[pId][0] for pId in PIECES_ID_TO_STR},
                self.numBoardAnalyses
            ),
            getAvgOf2Dicts(
                self.data[3],
                {pId: threatenedAndProtectedByP1[pId][0] for pId in PIECES_ID_TO_STR},
                self.numBoardAnalyses
            ),
            getAvgOf2Dicts(
                self.data[4],
                {pId: threatenedAndProtectedByP0[pId][1] for pId in PIECES_ID_TO_STR},
                self.numBoardAnalyses
            ),
            getAvgOf2Dicts(
                self.data[5],
                {pId: threatenedAndProtectedByP1[pId][1] for pId in PIECES_ID_TO_STR},
                self.numBoardAnalyses
            ),
        ]
        # TODO: simplify this with list comprehension, + operator and zip of ranges

    def getMove(self, gh, legalMovesPositions):
        self.numBoardAnalyses += 1

        if self.analyzeBoard:
            self.doBoardAnalysis(gh, legalMovesPositions)

        moveStr = self.move[self.numBoardAnalyses]

        try:
            move2 = Move(moveStr, self.side, (0,0))
        except ValueError:
            print(traceback.format_exc())
            print("Invalid move. Try again \n")
            return self.getMove(gh, legalMovesPositions)

        piecesPosIndex = None
        for i, movesYX in enumerate(legalMovesPositions[move2.p].values()):
            if (move2.y, move2.x) in movesYX:
                piecesPosIndex = i
                break

        if piecesPosIndex == None:
            print("Invalid move!\n ")

        piecePos = tuple(gh.board.piecesPos[self.side][move2.p][piecesPosIndex])

        move = Move(moveStr, self.side, piecePos)

        # determines the move, and which piece is used for it
        return piecesPosIndex, piecePos, move



