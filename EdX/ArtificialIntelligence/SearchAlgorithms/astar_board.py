from board import Board

class AStarBoard(Board):
	def __init__(self, board_state, direction, depth, cost, board_size, parent_board):
		Board.__init__(self, board_state, direction, depth, cost, board_size, parent_board)

	def get_total_manhattan_dist(self):
		total_dist = 0
		for i in range(0, len(self._board_state)):
			curr_row, curr_col = self._get_row_col(i)
			des_row, des_col = self._get_row_col(self._board_state[i])
			total_dist += abs(des_row - curr_row) + abs(des_col - curr_col)
		return total_dist

	def _get_new_board(self, board_state, direction, depth, cost, board_size, parent_board):
		return AStarBoard(board_state, direction, depth, cost, board_size, parent_board)

	