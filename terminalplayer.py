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
        self.needsAllLegalMoves = True


    def getMove(self, board: ChessBoard, legalMovesPositions: tuple):

        print(str(board))

        moveStr = input(f"Your Move ({self.color}): ")
        try:
            move2 = Move(moveStr, self.side, (0,0))
        except ValueError:
            print(traceback.format_exc())
            print("Invalid move. Try again \n")
            return self.getMove(board)

        if len([True for movesYX in legalMovesPositions[move2.p].values() if (move2.y, move2.x) in movesYX]) > 1:
            optionStr = ""
            print(board.piecesPos[self.side])
            
            for i in range(len(board.piecesPos[self.side][move2.p])):
                # piecePos is wrong
                print(board.piecesPos[self.side][move2.p][i])
                p1YX = board.piecesPos[self.side][move2.p][i]
                p1Pos = convertToStrMoveXY(p1YX)
                optionStr += f"\n  {i} = {p1Pos}"

            try:
                piecesPosIndex = int(input(f"Which piece? {optionStr} \n  ->"))
            except:
                piecesPosIndex = int(input(f"\nTry again: Which piece? {optionStr} \n  ->"))
        else:
            piecesPosIndex = None
            for i, movesYX in enumerate(legalMovesPositions[move2.p].values()):
                if (move2.y, move2.x) in movesYX:
                    piecesPosIndex = i

        # print(piecesPosIndex)

        piecePos = tuple(board.piecesPos[self.side][move2.p][piecesPosIndex])

        move = Move(moveStr, self.side, piecePos)

        # determines the move, and which piece is used for it
        return piecesPosIndex, piecePos, move



