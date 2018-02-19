from fringe import Fringe
from collections import deque


class BFSFringe(Fringe):
	def __init__(self):
		self.queue = deque([])

	def add_boards(self, boards):
		# boards are in U,D,L,R order. Push elements to queue in order
		for b in boards:
			self.queue.appendleft(b)

	def get_next_board(self):
		if (len(self.queue) > 0):
			return self.queue.pop()
		else:
			raise Exception("no more elements left in BFS fringe")

	def get_size(self):
		return len(self.queue)