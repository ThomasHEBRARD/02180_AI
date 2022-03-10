from __future__ import print_function

import os
import os.path
import math
import time
import random
import copy
import strategy as ai
import numpy as np

# from joblib import Parallel, delayed


from colorama import init, Fore, Style

init(autoreset=True)

import keypress
from board import Board


class Game(object):
    """
    A 2048 game
    """

    __clear = "cls" if os.name == "nt" else "clear"

    # see Game#adjustColors
    # these are color replacements for various modes

    def __init__(
        self,
        scores_file=SCORES_FILE,
        colors=COLORS,
        store_file=STORE_FILE,
        clear_screen=True,
        mode=None,
        azmode=False,
        **kws
    ):
        self.board = Board(**kws)
        self.score = 0
        self.scores_file = scores_file
        self.store_file = store_file
        self.clear_screen = clear_screen

        self.__colors = colors
        self.__azmode = azmode

        self.loadBestScore()
        self.adjustColors(mode)

    def incScore(self, pts):
        """
        update the current score by adding it the specified number of points
        """
        self.score += pts
        if self.score > self.best_score:
            self.best_score = self.score

    def loop(self, strategy=None, delay=None, max_depth=None, max_iters=None):
        """
        main game loop. returns the final score.
        """
        pause_key = self.board.PAUSE
        margins = {"left": 4, "top": 4, "bottom": 4}

        start_time = time.time()
        number_of_moves = 0
        try:
            while True:
                # only print if there's a delay or human player
                if delay or strategy is None:
                    if self.clear_screen:
                        os.system(Game.__clear)
                    else:
                        print("\n")
                    print(self.__str__(margins=margins))
                if self.board.won() or not self.board.canMove():
                    break

                # select move based on strategy employed
                if strategy == "random":
                    m = ai.random_move(self.board)
                    if delay:
                        time.sleep(delay)
                elif strategy == "priority":
                    m = ai.priority_move(self.board)
                    if delay:
                        time.sleep(delay)
                elif strategy == "mcts":
                    mcts = MCTS(self.board, max_depth=max_depth, max_iters=max_iters)
                    m = mcts.search()

                    if delay:
                        time.sleep(delay)
                else:
                    m = self.readMove()
                number_of_moves += 1

                if m == pause_key:
                    self.saveBestScore()
                    if self.store():
                        print(
                            "Game successfully saved. "
                            "Resume it with `term2048 --resume`."
                        )
                        return self.score
                    print("An error occurred while saving your game.")
                    return

                self.incScore(self.board.move(m))

        except KeyboardInterrupt:
            self.saveBestScore()
            return

        self.saveBestScore()
        if delay or strategy is None:
            print("You won!" if self.board.won() else "Game Over")
        total_time = time.time() - start_time
        return self.score, total_time, number_of_moves

    def getCellStr(self, x, y):  # TODO: refactor regarding issue #11
        """
        return a string representation of the cell located at x,y.
        """
        c = self.board.getCell(x, y)

        if c == 0:
            return "." if self.__azmode else "  ."

        elif self.__azmode:
            az = {}
            for i in range(1, int(math.log(self.board.goal(), 2))):
                az[2**i] = chr(i + 96)

            if c not in az:
                return "?"
            s = az[c]
        elif c == 1024:
            s = " 1k"
        elif c == 2048:
            s = " 2k"
        else:
            s = "%3d" % c

        return self.__colors.get(c, Fore.RESET) + s + Style.RESET_ALL
