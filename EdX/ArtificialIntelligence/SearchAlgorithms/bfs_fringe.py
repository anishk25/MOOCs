from fringe import Fringe
from collections import deque


class BFSFringe(Fringe):
	def __init__(self):
		self.__queue = deque([])

	def add_boards(self, boards):
		# boards are in U,D,L,R order. Push elements to queue in order
		for b in boards:
			self.__queue.appendleft(b)

	def get_next_board(self):
		if (len(self.__queue) == 0):
			raise Exception("no more elements left in BFS fringe")	
		return self.__queue.pop()

	def get_size(self):
		return len(self.__queue)