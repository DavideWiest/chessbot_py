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
        self.allLegalMoves = {}
        for pieceId in board.piecesPos[side]:
            # testing
            # print("PID")
            # print(pieceId)
            for pieceIndex, piecePos in enumerate(board.piecesPos[side][pieceId]):
                # print("PIN")
                # print(pieceIndex)
                
                self.allLegalMoves[(pieceId, pieceIndex)] = PIECES_ID_TO_CLASS[pieceId].getLegalMoves(board.board, tuple(piecePos), side, board.piecesPos, pieceId, pieceIndex, board.boardInfo)
    
                print(PIECES_ID_TO_STR[pieceId])
                print(len(self.allLegalMoves[(pieceId, pieceIndex)]))
                print(len(set(self.allLegalMoves[(pieceId, pieceIndex)])))
                print("----")

        if sum(len(pieceMoves) for pieceMoves in self.allLegalMoves.values()):
            self.winner = "black" if side == "white" else "white"


    def isValidMove(self, position: tuple, move: Move, pieceIndex: int):

        legalMovesOfPiece = self.allLegalMoves.get((move.p, pieceIndex), [])

        print(self.allLegalMoves)
        print(legalMovesOfPiece)

 
        return (position[0]+move.y, position[1]+move.x) in legalMovesOfPiece

    def isMatchFinished(self):
        return self.winner != None

    def getWinner(self):
        return self.winner