from game.board import *
from game.pieces import *
from game.player import *
from game.move import *
from game.referee import *

from datetime import datetime

import terminalplayer

class GameHandler():

    def __init__(self, playerWhite: Player, playerBlack: Player, gamesDir, autoSaveGame: str):
        self.pW = playerWhite
        self.pB = playerBlack

        self.autoSaveGame = autoSaveGame
        self.autoSaveDT = datetime.now().strftime("%d-%m-%Y-%H-%M")

        self.board = ChessBoard(gamesDir)
        self.referee = Referee()

    def run(self):
        
        self.index = 0

        # to implement 
        while self.referee.matchContinues():
            self.handleSingleMove()

        winner = self.referee.getWinner()
        print(f"Game finished. {winner} won")

    def handleSingleMove(self):
        currentPlayer, currentPlayerColor = (self.pB, COLORSTR_SIDE(self.pB.side)) if self.index % 2 == 0 else (self.pW, COLORSTR_SIDE(self.pW.side))
        print(f"Move {self.index+1} - {currentPlayerColor.capitalize()}'s turn \n\n")

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

        if self.autoSaveGame == "y" or self.autoSaveGame == "s" and self.index % 5 == 1:
            self.board.saveGame(self.autoSaveDT)
    

GAMES_DIR = "games"

if __name__ == "__main__":
    # run game

    available_players = {
        1: terminalplayer.TerminalPlayer
    }

    print("available players:")
    print("\n".join(f"{k}: {v}" for k,v in available_players.items()))

    playerBlack = available_players[int(input("Player black: "))](0, "yellow")
    playerWhite = available_players[int(input("Player white: "))](1, "green")

    loadGame = input("Filename of game to load (optional): ")
    autoSaveGame = input("Autosave (y / n / s = every 5th move) (optional, default n): ")
    assert autoSaveGame in ("y", "n", "s")

    gh = GameHandler(playerWhite, playerBlack, GAMES_DIR, autoSaveGame)

    if loadGame != "":
        gh.board.loadGame(loadGame)

    gh.run()