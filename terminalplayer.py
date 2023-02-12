from game.board import *
from game.pieces import *
from game.player import *
from game.move import *
from game.referee import *

import traceback

class TerminalPlayer(Player):

    def __init__(self, side: int, color: str):
        self.side = side
        self.color = color
        self.needsValidityChecked = True
        self.needsAllLegalMoves = False

    def printBoard(self, board: ChessBoard):
        print(str(board))

    def getMove(self, board: ChessBoard):

        piecesPos = board.piecesPos

        self.printBoard(board)

        move = input(f"Your Move ({self.color}): ")
        try:
            move2 = Move(move, self.side, (0,0))
        except ValueError:
            print(traceback.format_exc())
            print("Invalid move. Try again \n")
            return self.getMove(board)

        if len(piecesPos[move2.side][move2.p]) > 1:
            optionStr = ""
            for i in range(len(piecesPos[move2.side][move2.p])):
                p1X = piecesPos[move2.side][move2.p][i][0]
                p1Y = piecesPos[move2.side][move2.p][i][1]
                p1Pos = convertToStrMoveXY((p1X, p1Y+1))
                optionStr += f"\n{i}={p1Pos}"

            try:
                piecesPosIndex = int(input(f"Which piece? {optionStr} \n ->"))
            except:
                piecesPosIndex = int(input(f"Try again: Which piece? {optionStr} \n ->"))
        else:
            piecesPosIndex = 0

        piecePos = (
                piecesPos[move2.side][move2.p][piecesPosIndex][0],
                piecesPos[move2.side][move2.p][piecesPosIndex][1]
        )

        move = Move(move, self.side, piecePos)

        # determines the move, and which piece is used for it
        return piecesPosIndex, piecePos, move