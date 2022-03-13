import copy
import random
import numpy as np

from board import Board
from utils import compress, merge, reverse, transp


class ElJuego:
    def __init__(self, board):
        self.score = 0
        self.goal = 10000
        self.won, self.lost = False, False

        self.board = board

    def check_win(self):
        """
        Changes the win variable to True if the player won
        """
        if self.score >= self.goal:
            self.won = True

    def check_lost(self):
        """
        Changes the lost variable to True if the player lost
        """
        if len(self.board.get_available_moves()) == 0:
            self.lost = True

    def mcts(self):
        max_depth = 10
        available_moves = self.board.get_available_moves()

        move_score = {move: 0 for move in self.board.moves}
        move_count = {move: 0 for move in self.board.moves}

        for i in range(1000):
            possible_move = random.choice(available_moves)
            possible_grid = copy.copy(self.board)
            possible_game = ElJuego(possible_grid)
            depth = 0

            while True:
                if possible_game.won or possible_game.lost or depth > max_depth:
                    move_score[possible_move] += possible_game.score
                    move_count[possible_move] += 1
                    break

                if depth == 0:
                    next_move = possible_move
                else:
                    available_moves = possible_grid.get_available_moves()
                    next_move = random.choice(available_moves)

                possible_game.score += possible_grid.move(next_move)
                depth += 1

        move_count = {k: v if v != 0 else 1 for k, v in move_count.items()}
        result = {
            move: move_score[move] / move_count[move] for move in self.board.moves
        }
        chosen_move = max(result, key=result.get)
        return chosen_move

    def play(self):
        while not (self.lost or self.won):
            move = self.mcts()
            score_to_add = self.board.move(move)

            self.check_win()

            if self.won:
                self.display(move)
                break

            # Check if there are empty cells
            if self.board.empty_cell():
                self.board.new_values()

            self.check_lost()

            if self.lost:
                self.display(move)
                break
            # self.display(move)
            self.score += score_to_add
            print("Move: " + move + ",    Score: " + str(self.score))

        print("YOU LOSE" if self.lost else "YOU WIN")

    def display(self, move):
        """
        This is the ui: dislays the board and some info in the terminal
        """
        print("-----------------------------------------")
        print("Score: " + self.score + "   " + "Move that was done: " + move)
        print("")

        for row in self.board.grid:
            print(
                "{:<10s} {:<10s} {:<10s} {:<10s}".format(
                    *[str(r) if r != 0 else "." for r in row]
                )
            )


board = Board()
juego = ElJuego(board)

juego.play()
