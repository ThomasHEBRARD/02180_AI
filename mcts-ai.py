import numpy as np

def mcts(grid, max_depth):
    available_moves = grid.get_available_moves()

    move_score = [0, 0, 0, 0]
    move_count = [0, 0, 0, 0]

    for i in range(1000):
        possible_move = random.choice(available_moves)

        possbiel_grid = grid.copy()