class ElJuego:
    def __init__(self, board):
        self.score = 0
        self.goal = 1000
        self.won, self.lost = False, False

        self.board = board

    def check_win(self):
        """
        Changes the win variable to True if the player won
        """
        if self.score >= self.goal:
            if self.board.winning_tile():
                return True

    def check_lost(self):
        """
        Changes the lost variable to True if the player lost
        """
        if len(self.board.get_available_moves()) == 0:
            self.lost = True

    def play(self):
        while not (self.lost or self.won):
            next_move = self.board.find_next_move()
            score_to_add = self.board.move(next_move)

            self.check_win()

            if self.won:
                self.display(next_move)
                break

            # Check if there are empty cells
            if self.board.empty_cell():
                self.board.new_values()

            self.check_lost()

            if self.lost:
                self.display(next_move)
                break

            self.display(next_move)
            self.score += score_to_add
            print("Move: " + next_move + ",    Score: " + str(self.score))

        print("YOU LOSE" if self.lost else "YOU WIN")

    def display(self, move):
        """
        This is the ui: dislays the board and some info in the terminal
        """
        print("-----------------------------------------")
        print("Score: " + str(self.score) + "   " + "Move that was done: " + move)
        print("")

        for row in self.board.grid:
            print(
                "{:<10s} {:<10s} {:<10s} {:<10s}".format(
                    *[str(r) if r != 0 else "." for r in row]
                )
            )
