from fringe import Fringe

class DFSFringe(Fringe):

	def __init__(self):
		self.stack = []

	def add_boards(self, boards):
		# boards are in U,D,L,R order. Push elements to stack in reverse order
		for i in range(len(boards) - 1, -1, -1):
			self.stack.append(boards[i])

	def get_next_board(self):
		if (len(self.stack) > 0):
			return self.stack.pop()
		else:
			raise Exception("no more elements left in DFS fringe")

	def get_size(self):
		return len(self.stack)
