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
        
        self.lastMove = None
        self.index = 1

        # to implement 
        while not self.referee.isMatchFinished():
            self.handleSingleMove()

        winner = self.referee.getWinner()
        print(f"Game finished. {winner} won")

    def handleSingleMove(self):
        currentPlayer, currentPlayerStr = playerWhite, "white" if self.index % 2 == 1 else playerBlack, "black"
        print(f"Move {self.index} - {currentPlayerStr}'s turn \n\n")

        piecePos, move = currentPlayer.getMove(self.board.board, self.board.piecesPos)

        if currentPlayer.needsValidityChecked:
            if not self.referee.isValidMove(move):
                self.handleSingleMove()
            else:
                self.index += 1
        else:
            self.index += 1

        self.board.makeMove(piecePos, move, currentPlayer.side)

        self.lastMove = move

if __name__ == "__main__":
    # run game

    available_players = {
        1: terminalplayer
    }

    print("available players:")
    print(available_players)

    playerWhite = available_players[int(input("Player white: "))](0)
    playerBlack = available_players[int(input("Player black: "))](1)

    gh = GameHandler(playerWhite, playerBlack)
    gh.run()