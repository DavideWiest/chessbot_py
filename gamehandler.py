from game.board import *
from game.pieces import *
from game.player import *
from game.move import *
from game.referee import *

from datetime import datetime
import sys
import time

import terminalplayer
import algoplayer
import algoplayerchecking

class GameHandler():

    def __init__(self, playerWhite: Player, playerBlack: Player, gamesDir, autoSaveGame: str, autoSaveFilename: str="", timebuffer: int=0):
        self.pW = playerWhite
        self.pB = playerBlack
        
        self.autoSaveGame = autoSaveGame
        self.timebuffer = timebuffer

        self.board = ChessBoard(gamesDir)
        self.referee = Referee()
        
        if autoSaveFilename == "":
            self.autoSaveFilename = datetime.now().strftime("%d-%m-%Y-%H-%M")
            self.index = 0
        else:
            self.autoSaveFilename = autoSaveFilename
            try:
                self.index = self.board.loadGameReturnMoveIndex(autoSaveFilename)
            except NoSuchGameSaved:
                self.index = 0

    def run(self):
        
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
            piecesPosIndex, piecePos, move = currentPlayer.getMove(self, self.referee.allLegalMoves)
        else:
            piecesPosIndex, piecePos, move = currentPlayer.getMove(self)

        if currentPlayer.needsValidityChecked:
            if not self.referee.isValidMove(move, piecesPosIndex): 
                print("\n -> Invalid move! \n")
                return
        
        self.index += 1

        self.board.makeMove(piecePos, move, True)

        if len(self.board.piecePos[OTHERSIDE(move.side)][KING]) == 0:
            self.referee.setWinner(OTHERSIDE(move.side))

        self.board.boardInfo[currentPlayer.side]["lastMovePos"] = (move.y, move.x)

        if self.autoSaveGame == "y" or self.autoSaveGame == "s" and self.index % 5 == 1:
            self.board.saveGame(self.autoSaveFilename, self.index)

        if self.timebuffer:
            time.sleep(self.timebuffer)

GAMES_DIR = "games"

if __name__ == "__main__":
    # run game

    available_players = [
        terminalplayer.TerminalPlayer,
        algoplayer.AlgoPlayer,
        algoplayerchecking.AlgoPlayerChecking
    ]

    if len(sys.argv) > 2:
        condition = sys.argv[-2].isnumeric() and sys.argv[-1].isnumeric()
    else:
        condition = False

    if condition:
        player0Id = int(sys.argv[-2])
        player1Id = int(sys.argv[-1])
    else:
        print("available players:")
        print("\n".join(f"{i}: {v}" for i,v in enumerate(available_players)))

        player0Id = int(input(f"Player {COLORSTR_SIDE(0)}: "))
        player1Id = int(input(f"Player {COLORSTR_SIDE(1)}: "))

    playerBlack = available_players[player0Id](0, COLORSTR_SIDE(0))
    playerWhite = available_players[player1Id](1, COLORSTR_SIDE(1))

    gameFilename = input("Filename of game to load (optional): ")
    autoSaveGame = input("Autosave (y / n / s = every 5th move) (optional, default n): ")
    if autoSaveGame not in ("y", "s"):
        autoSaveGame = "n"
    
    timebuffer = input("Time buffer (input in s, default 0): ")
    if not timebuffer.isnumeric():
        timebuffer = 0

    gh = GameHandler(playerWhite, playerBlack, GAMES_DIR, autoSaveGame, gameFilename, timebuffer)

    gh.run()

