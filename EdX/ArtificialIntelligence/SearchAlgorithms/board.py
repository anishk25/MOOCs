class Board:
	def __init__(self, board_state, moves, depth, cost, board_size):
		self._board_state = board_state
		self._moves = moves
		self._depth = depth
		self._cost = cost
		self._board_size = board_size

	def is_solved(self):
		l = self._board_state
		return all(l[i] <= l[i+1] for i in xrange(len(l)-1))

	def get_next_states(self):
		empty_cell_index = self._board_state.index(0)
		row, col = self._get_row_col(empty_cell_index)

		next_states = []
		self.__add_board_to_lst(empty_cell_index, row - 1, col, 'Up', next_states)
		self.__add_board_to_lst(empty_cell_index, row + 1, col, 'Down', next_states)
		self.__add_board_to_lst(empty_cell_index, row, col - 1, 'Left', next_states)
		self.__add_board_to_lst(empty_cell_index, row, col + 1, 'Right', next_states)

		return next_states

	def get_formatted_board_string(self):
		board_str = ""
		for i in range(0, len(self._board_state)):
			board_str += str(self._board_state[i])
			rem = (i + 1) % self._board_size
			if (rem == 0):
				if (i != len(self._board_state) - 1):
					board_str += '\n'
			else:
				board_str += '\t'	
		return board_str

	def __add_board_to_lst(self, empty_cell_index, new_row, new_col, direction, states):
		if (new_row >= 0 and new_row < self._board_size and new_col >= 0 and new_col < self._board_size):
			new_cell_index = self.__get_index(new_row, new_col)
			new_board_state = self._board_state[:]
			new_moves = self._moves[:] + [direction]
			self.__switch_indices(new_board_state, empty_cell_index, new_cell_index)
			new_board = self._get_new_board(new_board_state, new_moves, self._depth + 1, self._cost + 1, self._board_size)
			states.append(new_board)

	def _get_row_col(self, index):
		return (index / self._board_size, index % self._board_size)

	def __get_index(self, row, col):
		return (self._board_size * row) + col

	def __switch_indices(self, lst, index1, index2):
		temp = lst[index1]
		lst[index1] = lst[index2]
		lst[index2] = temp

	def _get_new_board(self, board_state, moves, depth, cost, board_size):
		return Board(board_state, moves, depth, cost, board_size)

	def __hash__(self):
		return hash(tuple(self._board_state))

	def __eq__(self, other):
		return self._board_state == other.board_state

	def __str__(self):
		return 'Board State: %s , Moves: %s, Depth: %d, Cost: %d, Board Size: %d' % \
				(str(self._board_state), str(self._moves), self._depth, self._cost, self._board_size)

	

	@property
	def board_state(self):
		return self._board_state

	@property
	def moves(self):
		return self._moves


	@property
	def depth(self):
		return self._depth

	@property
	def cost(self):
		return self._cost





