from game.board import *
from game.pieces import *
from game.player import *
from game.move import *

class Referee():

    def __init__(self):
        self.winner = None
        self.allLegalMoves = {}
        pass

    def computeAllLegalMoves(self, board: ChessBoard, side: int):
        self.allLegalMoves = {
            pId: {} for pId in list(PIECES_ID_TO_STR)
        }
        for pieceId in board.piecesPos[side]:
            for pieceIndex, piecePos in enumerate(board.piecesPos[side][pieceId]):
                self.allLegalMoves[pieceId][pieceIndex] = PIECES_ID_TO_CLASS[pieceId].getLegalMoves(board.board, tuple(piecePos), side, board.piecesPos, pieceId, pieceIndex, board.boardInfo)
    
                # board.visualizeLegalMoves(pieceId, pieceIndex, side, 2, self.allLegalMoves[pieceId][pieceIndex])
                # print(PIECES_ID_TO_NAME[pieceId])
                # print("----")

        # piece moves sum by piece id
        print(self.allLegalMoves)

        # sum of all possible moves
        print(sum(
            sum(len(moves) for moves in piecesMovesById.values()) 
            for piecesMovesById in self.allLegalMoves.values()
        ))

        if sum(
            sum(len(moves) for moves in piecesMovesById.values()) 
            for piecesMovesById in self.allLegalMoves.values()
        ) < 1:
            print("winner has been")
            self.winner = "black" if side == "white" else "white"


    def isValidMove(self, move: Move, pieceIndex: int):

        legalMovesOfPiece = self.allLegalMoves.get(move.p, {}).get(pieceIndex, [])

        return (move.y, move.x) in legalMovesOfPiece

    def matchContinues(self):
        "false if match is finished"
        return self.winner == None

    def getWinner(self):
        return self.winner