from fringe import Fringe
from board import Board
from collections import defaultdict
import heapq

class AStarFringe(Fringe):
	def __init__(self):
		self.__priority_que = []

	def add_boards(self, boards):
		for b in boards:
			manhattan_dist = b.get_total_manhattan_dist()
			total_cost = manhattan_dist + b.cost
			heapq.heappush(self.__priority_que, (total_cost, b))

	def get_next_board(self):
		if (len(self.__priority_que) == 0):
			raise Exception("no more elements left in A Star fringe")

		tied_boards = defaultdict(list)

		min_score, _ = self.__priority_que[0] # peeking at top of the queue
		while(self.__priority_que[0][0] == min_score && self.get_size() > 0):
			score, board = heapq.heappop(self.__priority_que)
			direction = board.moves[len(board.moves) - 1]
			heapq.heappush(tied_boards[direction], (board.cost, score, board))

		selected_board = None
		for direction in Board.MOVES_ORDER:
			if (len(tied_boards[direction]) > 0):
				_,_,selected_board = heapq.heappop(tied_boards[direction])
				break

		for direction in Board.MOVES_ORDER:
			for _,score,board in tied_boards[direction]
				heapq.heappush(self.__priority_que, (score, board))

		return selected_board



	def get_size(self):
		return len(self.__priority_que)