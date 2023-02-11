import game

class TerminalPlayer(game.Player):

    def __init__(self, side: int):
        self.side = side
        self.needsMoveChecked = True

    def printBoard(self, board: game.ChessBoard):
        print(board)

    def getMove(self, board: game.ChessBoard, piecePos):

        self.printBoard(board)

        move = input("Your Move: ")
        try:
            move = game.Move(move, self.side, (0,0))
        except ValueError:
            print("Invalid move. Try again \n")
            return self.getMove(board, piecePos)

        if move.p not in (9,10) and len(piecePos[move.side][move.p]) > 1:
            optionStr = ""
            for i in range(len(piecePos[move.side][move.p])):
                p1X = piecePos[move.side][move.p][i][0]
                p1Y = piecePos[move.side][move.p][i][1]
                p1Pos = game.convertToStrMoveXY((p1X-1, p1Y))
                optionStr += f"\n{i}={p1Pos}"

            try:
                piecePosIndex = int(input(f"Which piece? {optionStr} \n ->"))
            except:
                piecePosIndex = int(input(f"Try again: Which piece? {optionStr} \n ->"))

            piecePos = (
                piecePos[move.side][move.p][piecePosIndex][0],
                piecePos[move.side][move.p][piecePosIndex][1]
            )

        return piecePos, move