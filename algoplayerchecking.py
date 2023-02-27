from game.board import *
from game.pieces import *
from game.player import *
from game.move import *
from game.referee import *

import time

from algoplayer import AlgoPlayer

class AlgoPlayerChecking(AlgoPlayer):

    def validateMove(self, move: Move):
        isValid = input(f"Valid move? (y/n, default y) \n {str(move)}\n ->")
        if (isValid or "y") == "y":
            return True

        return False

    def wait(self):
        time.sleep(1)
