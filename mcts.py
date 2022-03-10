import random
import numpy as np

def mcts(grid):
    available_moves = grid.get_available_moves()

    move_score = [0, 0, 0, 0]
    move_count = [0, 0, 0, 0]

    for i in range(1000):
        possible_move = random.choice(available_moves)

        possbiel_grid = grid.grid.copy()



class MCTS(object):
	"""
	run mcts to find best move
	"""
	def __init__(self, board, max_depth, max_iters):
		self.max_depth = max_depth
		self.max_iters = max_iters
		self.board = board
		# self.n_jobs = n_jobs
		# self.verbose = verbose

	def search(self):
		# loop for max_iters
		available_branches = self.board.get_valid_moves()
		branch_scores = [0] * 4
		branch_counts = [0] * 4

		
		for i in xrange(self.max_iters):
			# randomly select a branch to search down
			branch = random.choice(available_branches)
			board_sim = copy.deepcopy(self.board)
			game_sim = Game(board_sim)
			depth = 0
			while True:
				if board_sim.won() or not board_sim.canMove() or depth > self.max_depth:
					branch_scores[(branch - 1)] += game_sim.score
					branch_counts[(branch - 1)] += 1
					break
				# first move is down the selected branch
				if depth == 0:
					next_move = branch
				else:
					# otherwise play out randomly
					available_moves = board_sim.get_valid_moves()
					next_move = random.choice(available_moves)
				# keep track of score based on move selection
				game_sim.incScore(board_sim.move(next_move))
				depth += 1

		# select move corresponding to best branch score
		branch_counts = np.array(branch_counts)
		branch_counts = np.where(branch_counts == 0, 1.0, branch_counts) # avoid divide by zero
		branch_results = np.array(branch_scores) / branch_counts
		move = np.where(branch_results == np.max(branch_results))[0][0] + 1
		return move