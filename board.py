import copy
import random
import numpy as np

from utils import compress, reverse, transp, merge
from game import ElJuego

MEMO = {}

class Board:
    def __init__(self):
        self.moves = ["UP", "DOWN", "LEFT", "RIGHT"]

        self.grid = np.zeros((4, 4), dtype=int)

        # First random values
        i_1 = [random.randint(0, 3), random.randint(0, 3)]
        i_2 = [random.randint(0, 3), random.randint(0, 3)]
        while i_2 == i_1:
            i_2 = [random.randint(0, 3), random.randint(0, 3)]

        self.grid[i_1[0]][i_1[1]], self.grid[i_2[0]][i_2[1]] = 2, 2

    def get_available_moves(self):
        """
        Returns all available moves from "UP", "DOWN", "LEFT", "RIGHT" (as an array)
        """

        return [move for move in self.moves if self.move_validity(move)]

    def empty_cell(self):
        """
        Return True if the grid contains at least one empty cell, else return False
        """

        for i in range(4):
            for j in range(4):
                if self.grid[i][j] == 0:
                    return True
        return False

    def move_validity(self, move):
        """
        Test if a given move is possible
        move can be "UP" or "DOWN" or "LEFT" or "RIGHT"
        """
        # des corrections faites pour interdire un mouvement si il n'y a que des zéros dans une colonne
        # possible de combiner up et down et left et right. A moins que j'ai pas capté un truc c'est deux fois le même algo
        if move == "UP":
            for col in self.get_all_columns():
                one_tile = False
                empty_tile = False
                for i in range(4):
                    if col[i] == 0:
                        empty_tile = True
                    else:
                        one_tile = True
                    if empty_tile and one_tile:
                        return True
                    if i < 3 and col[i] != 0 and col[i] == col[i + 1]:
                        return True
            return False

        if move == "DOWN":
            for col in self.get_all_columns():
                one_tile = False
                empty_tile = False
                for i in range(4):
                    if col[i] == 0:
                        empty_tile = True
                    else:
                        one_tile = True
                    if empty_tile and one_tile:
                        return True
                    if i < 3 and col[i] != 0 and col[i] == col[i + 1]:
                        return True
            return False

        if move == "LEFT":
            for row in self.get_all_rows():
                one_tile = False
                empty_tile = False
                for i in range(4):
                    if row[i] == 0:
                        empty_tile = True
                    else:
                        one_tile = True
                    if empty_tile and one_tile:
                        return True
                    if i < 3 and row[i] != 0 and row[i] == row[i + 1]:
                        return True
            return False

        if move == "RIGHT":
            for row in self.get_all_rows():
                one_tile = False
                empty_tile = False
                for i in range(4):
                    if row[i] == 0:
                        empty_tile = True
                    else:
                        one_tile = True
                    if empty_tile and one_tile:
                        return True
                    if i < 3 and row[i] != 0 and row[i] == row[i + 1]:
                        return True
            return False

    def get_all_rows(self):
        """
        Return all columns (left to right)
        """
        return [self.grid[row_index] for row_index in range(4)]

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

        self.grid[i][j] = random.choices([2, 4], [0.9, 0.1])[0]

    def move(self, move):
        """
        Carry out a move and checks for win/lose, and displays the new board
        """

        if move == "UP":
            return self.up()
        elif move == "DOWN":
            return self.down()
        elif move == "LEFT":
            return self.left()
        elif move == "RIGHT":
            return self.right()

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

    def find_next_move(self):
        if self.board_id(self.grid) in MEMO:
            return MEMO[self.board_id(self.grid)]

        max_depth = 10
        available_moves = self.get_available_moves()

        move_score = {move: 0 for move in self.moves}
        move_count = {move: 0 for move in self.moves}

        for _ in range(1000):
            # print(move_score, move_count)
            possible_move = random.choice(available_moves)
            possible_grid = copy.copy(self)
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
        result = {move: move_score[move] / move_count[move] for move in self.moves}
        chosen_move = max(result, key=result.get)
        MEMO[self.board_id(self.grid)] = chosen_move
        return chosen_move

