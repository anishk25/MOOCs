from fringe import Fringe
from collections import deque


class BFSFringe(Fringe):
	def __init__(self):
		Fringe.__init__(self)
		self.__queue = deque([])

	def add_boards(self, boards):
		# boards are in U,D,L,R order. Push elements to queue in order
		for b in boards:
			if (b not in self._fringe_set):
				self.__queue.appendleft(b)
				self._fringe_set.add(b)
			

	def get_next_board(self):
		if (len(self.__queue) == 0):
			raise Exception("no more elements left in BFS fringe")	
		b = self.__queue.pop()
		self._fringe_set.remove(b)
		return b

	def get_size(self):
		return len(self.__queue)