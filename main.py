import random
import numpy as np
from utils import compress, merge, reverse, transp


class Grid:
    def __init__(self):
        self.score = 0
        self.state = 0
        self.board = np.zeros((4, 4), dtype=int)
        i_1 = [random.randint(0, 3), random.randint(0, 3)]
        i_2 = [random.randint(0, 3), random.randint(0, 3)]
        while i_2 == i_1:
            i_2 = [random.randint(0, 3), random.randint(0, 3)]

        self.board[i_1[0]][i_1[1]], self.board[i_2[0]][i_2[1]] = 2, 2
        self.lost = False
        self.win = False
        self.display("")

    def have_win(self):
        if self.score >= 600:
            self.win = True

    def have_lost(self):
        for i in range(3):
            for j in range(3):
                if (
                    self.board[i][j] == self.board[i + 1][j]
                    or self.board[i][j] == self.board[i][j + 1]
                ):
                    pass

        for j in range(3):
            if self.board[3][j] == self.board[3][j + 1]:
                pass

        for i in range(3):
            if self.board[i][3] == self.board[i + 1][3]:
                pass

        self.lost = True

    def new_values(self):
        i, j = random.randint(0, 3), random.randint(0, 3)

        while self.board[i][j] != 0:
            i, j = random.randint(0, 3), random.randint(0, 3)

        new_val = random.choices([2, 4], [0.9, 0.1])[0]
        self.board[i][j] = new_val

    def move(self, move):
        if move == "UP":
            self.up()
        elif move == "DOWN":
            self.down()
        elif move == "LEFT":
            self.left()
        elif move == "RIGHT":
            self.right()

        self.have_win()

        if self.win:
            self.display(move)
            return

        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0:
                    self.new_values()
                    self.display(move)
                    self.state += 1
                    return

        self.display(move)
        self.state += 1
        self.have_lost()

    def left(self):
        arr1 = self.board.copy()

        arr2 = compress(arr1)
        arr3, self.score = merge(arr2, self.score)
        self.board = compress(arr3)

    def right(self):
        arr1 = self.board.copy()

        arr2 = reverse(arr1)
        arr3 = compress(arr2)
        arr4, self.score = merge(arr3, self.score)
        arr5 = compress(arr4)
        self.board = reverse(arr5)

    def up(self):
        arr1 = self.board.copy()

        arr2 = transp(arr1)
        arr3 = compress(arr2)
        arr4, self.score = merge(arr3, self.score)
        arr5 = compress(arr4)
        self.board = transp(arr5)

    def down(self):
        arr1 = self.board.copy()

        arr2 = transp(arr1)
        arr3 = reverse(arr2)
        arr4 = compress(arr3)
        arr5, self.score = merge(arr4, self.score)
        arr6 = compress(arr5)
        arr7 = reverse(arr6)
        self.board = transp(arr7)

    def display(self, move):
        print("-----------------------------------------")
        print(
            "State: "
            + str(self.state)
            + "       "
            + "Score: "
            + str(self.score)
            + "      "
            + "Move that was done: "
            + move
        )
        print("")
        for row in self.board:
            print(
                "{:<10s} {:<10s} {:<10s} {:<10s}".format(
                    *[str(r) if r != 0 else "." for r in row]
                )
            )


g = Grid()

while not (g.lost or g.win):
    g.move(random.choice(["UP", "DOWN", "LEFT", "RIGHT"]))

print("YOU LOSE" if g.lost else "YOU WIN")
