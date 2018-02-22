from fringe import Fringe

class DFSFringe(Fringe):

	def __init__(self):
		Fringe.__init__(self)
		self.__stack = []

	def add_boards(self, boards):
		# boards are in U,D,L,R order. Push elements to stack in reverse order
		for i in range(len(boards) - 1, -1, -1):
			if boards[i] not in self._fringe_set:
				self.__stack.append(boards[i])
				self._fringe_set.add(boards[i])

	def get_next_board(self):
		if (len(self.__stack) == 0):
			raise Exception("no more elements left in DFS fringe")
		b = self.__stack.pop()
		self._fringe_set.remove(b)
		return b

	def get_size(self):
		return len(self.__stack)
