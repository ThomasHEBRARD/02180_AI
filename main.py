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

##        self.board[i_1[0]][i_1[1]], self.board[i_2[0]][i_2[1]] = 2, 2

        self.board[0][2] = 2
        self.board[0][3] = 2
        self.board[0][0] = 2
        self.board[3][2] = 2

        self.board[2][1] = 10
        self.board[2][2] = 10

        self.display()

    def new_values(self):
        ij = [random.randint(0, 3), random.randint(0, 3)]
        while self.board[ij[0]][ij[1]] != 0:
            ij = [random.randint(0, 3), random.randint(0, 3)]
        self.board[ij[0]][ij[1]] = random.choices([2, 4], [0.9, 0.1])[0]

    def left(self):
        arr1 = self.board.copy()

        arr2 = compress(arr1)
        arr3, self.score = merge(arr2, self.score)
        self.board = compress(arr3)

        self.new_values()
##        self.display()

    def right(self):
        arr1 = self.board.copy()

        arr2 = reverse(arr1)
        arr3 = compress(arr2)
        arr4, self.score = merge(arr3, self.score)
        arr5 = compress(arr4)
        self.board = reverse(arr5)

        self.new_values()
##        self.display()

    def up(self):
        arr1 = self.board.copy()

        arr2 = transp(arr1)
        arr3 = compress(arr2)
        arr4, self.score = merge(arr3, self.score)
        arr5 = compress(arr4)
        self.board = transp(arr5)

        self.new_values()
##        self.display()

    def down(self):
        arr1 = self.board.copy()

        arr2 = transp(arr1)
        arr3 = reverse(arr2)
        arr4 = compress(arr3)
        arr5, self.score = merge(arr4, self.score)
        arr6 = compress(arr5)
        arr7 = reverse(arr6)
        self.board = transp(arr7)

        self.new_values()
##        self.display()

    def display(self):
        print("-----------------------------------------")
        print("State: " + str(self.state) + "       " + "Score: " + str(self.score))
        print("")
        for row in self.board:
            print(
                "{:<10s} {:<10s} {:<10s} {:<10s}".format(
                    *[str(r) if r != 0 else "." for r in row]
                )
            )

        self.state += 1

    def ai(self, g):

        row_size = int(self.board.size / len(self.board[0]))
        for i in range(row_size):
            for j in range(row_size):

                if self.board[i][j] != 0:
                    g.is_row_matching(i, j)
                    g.is_column_matching(i, j)



    def is_row_matching(self, row, column):
        size = int(self.board.size / len(self.board[0]))
        if column == size-1:
##            print("last element")
            return

        value = self.board[row][column]
        i = column + 1
        while i < size:
            temp = self.board[row][i]
            if temp != 0:
                if temp == value:
                    print("matched")
                    return 1
                else:
##                    print("break")
                    break
            i += 1

    def is_column_matching(self, row, column):
        size = int(self.board.size / len(self.board[0]))
        if row == size-1:
##            print("last element (column)")
            return

        value = self.board[row][column]
        i = row + 1
        while i < size:
            temp = self.board[i][column]
            if temp != 0:
                if temp == value:
                    print("matched(column)")
                    return 1
                else:
##                    print("break(column)")
                    break
            i += 1
##        print("not matched")








g = Grid()
g.ai(g)


















