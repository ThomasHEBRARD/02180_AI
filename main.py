import random
import numpy as np

from mcts import mcts
from utils import compress, merge, reverse, transp


class ElJuego:
    def __init__(self, grid):
        self.score = 0
        self.board = grid
        self.goal = 60000

        self.won, self.lost = False, False

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
        if len(self.get_available_moves()) == 0:
            self.lost = True

    def play(self):
        while not (self.lost or self.won):
            move = mcts(self.board)
            score_to_add = self.board.move(move)

            self.check_win()

            if self.won:
                self.board.display(move)
                break

            # Check if there are empty cells
            for i in range(4):
                for j in range(4):
                    if self.board[i][j] == 0:
                        self.board.new_values()

            self.board.dislay(move)
            self.score += score_to_add

        print("done")


class Grid:
    def __init__(self):
        self.moves = ["UP", "DOWN", "LEFT", "RIGHT"]

        self.grid = np.zeros((4, 4), dtype=int)
        i_1 = [random.randint(0, 3), random.randint(0, 3)]
        i_2 = [random.randint(0, 3), random.randint(0, 3)]
        while i_2 == i_1:
            i_2 = [random.randint(0, 3), random.randint(0, 3)]

        self.grid[i_1[0]][i_1[1]], self.grid[i_2[0]][i_2[1]] = 2, 2

        self.display("Initial board")

    def get_available_moves(self):
        """
        Returns as an array the moves among ["UP", "DOWN", "LEFT", "RIGHT"] that are valid
        """
        available_moves = []
        for move in self.moves:
            if self.move_validity(move):
                available_moves.append(move)
        return available_moves

    def move_validity(self, move):
        """
        Test if a given move is possible
        move can be "UP" or "DOWN" or "LEFT" or "RIGHT"
        """

        if move == "UP":
            for col in self.get_all_columns():
                for i in range(4):
                    if col[i] == 0:
                        return True
                    if i < 3 and col[i] != 0 and col[i] == col[i + 1]:
                        return True
            return False

        if move == "DOWN":
            for col in self.get_all_columns():
                for i in range(4):
                    if col[3] == 0:
                        return True
                    if i < 3 and col[i] != 0 and col[i] == col[i + 1]:
                        return True
            return False

        if move == "LEFT":
            for row in self.get_all_rows():
                for i in range(4):
                    if row[0] == 0:
                        return True
                    if i < 3 and row[i] != 0 and row[i] == row[i + 1]:
                        return True
            return False

        if move == "RIGHT":
            for row in self.get_all_rows():
                for i in range(4):
                    if row[3] == 0:
                        return True
                    if i < 3 and row[i] != 0 and row[i] == row[i + 1]:
                        return True
            return False

    def get_specific_row(self, index):
        """
        Returns the row index, from left to right
        example:
        self.grid = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16]
        ]
        then grid.get_specific_row(2) will return [9, 10, 11, 12]
        """
        return list(list(self.grid)[index])

    def get_all_rows(self):
        """
        Return all columns (left to right)
        """
        return [self.get_specific_row(row_index) for row_index in range(4)]

    def get_specific_column(self, index):
        """
        Returns the column index, from top to bottom
        example:
        self.grid = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16]
        ]
        then grid.get_specific_column(2) will return [3, 7, 11, 15]
        """
        return [row[index] for row in self.grid]

    def get_all_columns(self):
        """
        Return all columns (top to bottom)
        """
        return [self.get_specific_column(col_index) for col_index in range(4)]

    def new_values(self):
        """
        Randomly add a 2 or 4
        """
        i, j = random.randint(0, 3), random.randint(0, 3)

        while self.grid[i][j] != 0:
            i, j = random.randint(0, 3), random.randint(0, 3)

        new_val = random.choices([2, 4], [0.9, 0.1])[0]
        self.grid[i][j] = new_val

    def move(self, move):
        """
        Carry out a move and checks for win/lose, and displays the new board
        """

        score_to_add = 0

        if move == "UP":
            score_to_add = self.up()
        elif move == "DOWN":
            score_to_add = self.down()
        elif move == "LEFT":
            score_to_add = self.left()
        elif move == "RIGHT":
            score_to_add = self.right()

        return score_to_add

    def left(self):
        """
        Move to the left
        """
        arr1 = self.grid.copy()

        arr2 = compress(arr1)
        arr3, score_to_add = merge(arr2)
        self.grid = compress(arr3)

        return score_to_add

    def right(self):
        """
        Move to the right
        """
        arr1 = self.grid.copy()

        arr2 = reverse(arr1)
        arr3 = compress(arr2)
        arr4, score_to_add = merge(arr3)
        arr5 = compress(arr4)
        self.grid = reverse(arr5)

        return score_to_add

    def up(self):
        """
        Move up
        """
        arr1 = self.grid.copy()

        arr2 = transp(arr1)
        arr3 = compress(arr2)
        arr4, score_to_add = merge(arr3)
        arr5 = compress(arr4)
        self.grid = transp(arr5)

        return score_to_add

    def down(self):
        """
        Move down
        """
        arr1 = self.grid.copy()

        arr2 = transp(arr1)
        arr3 = reverse(arr2)
        arr4 = compress(arr3)
        arr5, score_to_add = merge(arr4)
        arr6 = compress(arr5)
        arr7 = reverse(arr6)
        self.grid = transp(arr7)

        return score_to_add

    def display(self, move):
        """
        This is the ui: dislays the board and some info in the terminal
        """
        print("-----------------------------------------")
        print("Move that was done: " + move)
        print("")
        for row in self.grid:
            print(
                "{:<10s} {:<10s} {:<10s} {:<10s}".format(
                    *[str(r) if r != 0 else "." for r in row]
                )
            )

grid = Grid()
juedo = ElJuego(grid)

juedo.play()