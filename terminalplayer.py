from game.board import *
from game.pieces import *
from game.player import *
from game.move import *
from game.referee import *

class TerminalPlayer(Player):

    def __init__(self, side: int):
        self.side = side
        self.needsMoveChecked = True

    def printBoard(self, board: ChessBoard):
        print(board)

    def getMove(self, board: ChessBoard, piecesPos):

        self.printBoard(board)

        move = input("Your Move: ")
        try:
            move = game.Move(move, self.side, (0,0))
        except ValueError:
            print("Invalid move. Try again \n")
            return self.getMove(board, piecesPos)

        if move.p not in (9,10) and len(piecesPos[move.side][move.p]) > 1:
            optionStr = ""
            for i in range(len(piecesPos[move.side][move.p])):
                p1X = piecesPos[move.side][move.p][i][0]
                p1Y = piecesPos[move.side][move.p][i][1]
                p1Pos = game.convertToStrMoveXY((p1X-1, p1Y))
                optionStr += f"\n{i}={p1Pos}"

            try:
                piecesPosIndex = int(input(f"Which piece? {optionStr} \n ->"))
            except:
                piecesPosIndex = int(input(f"Try again: Which piece? {optionStr} \n ->"))
        else:
            piecesPosIndex = 0

        piecePos = (
                piecesPos[move.side][move.p][piecesPosIndex][0],
                piecesPos[move.side][move.p][piecesPosIndex][1]
        )

        move = Move(move, self.side, piecePos)

        return piecesPosIndex, piecePos, move