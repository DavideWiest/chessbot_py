from game.board import *
from game.pieces import *
from game.player import *
from game.move import *
from game.referee import *

import terminalplayer

class GameHandler():

    def __init__(self, playerWhite: Player, playerBlack: Player):
        self.pW = playerWhite
        self.pB = playerBlack

        self.board = ChessBoard()
        self.referee = Referee()

    def run(self):
        
        self.index = 1

        # to implement 
        while self.referee.matchContinues():
            self.handleSingleMove()

        winner = self.referee.getWinner()
        print(f"Game finished. {winner} won")

    def handleSingleMove(self):
        currentPlayer, currentPlayerStr = (playerWhite, "white") if self.index % 2 == 0 else (playerBlack, "black")
        print(f"Move {self.index} - {currentPlayerStr.capitalize()}'s turn \n\n")

        self.referee.computeAllLegalMoves(self.board, currentPlayer.side)

        if currentPlayer.needsAllLegalMoves:
            piecesPosIndex, piecePos, move = currentPlayer.getMove(self.board, self.referee.allLegalMoves)
        else:
            piecesPosIndex, piecePos, move = currentPlayer.getMove(self.board)

        if currentPlayer.needsValidityChecked:
            if not self.referee.isValidMove(move, piecesPosIndex): 
                print("\n -> Invalid move! \n")
                self.handleSingleMove()
            else:
                self.index += 1
        else:
            self.index += 1

        self.board.makeMove(piecePos, move, True)

        self.board.boardInfo["lastMovePos"] = (move.y, move.x)

if __name__ == "__main__":
    # run game

    available_players = {
        1: terminalplayer.TerminalPlayer
    }

    print("available players:")
    print("\n".join(f"{k}: {v}" for k,v in available_players.items()))

    playerWhite = available_players[int(input("Player white: "))](0, "green")
    playerBlack = available_players[int(input("Player black: "))](1, "yellow")

    gh = GameHandler(playerWhite, playerBlack)
    gh.run()