from board import Board
from astar_board import AStarBoard
from math import sqrt
from dfs_fringe import DFSFringe
from bfs_fringe import BFSFringe
from astar_fringe import AStarFringe
import sys
import time
import resource
from collections import deque


BFS_OPTION = 'bfs'
DFS_OPTION = 'dfs'
ASTAR_OPTION = 'ast'

OUTPUT_FILE_NAME = 'output.txt'

FRINGE_OPTIONS = {BFS_OPTION   : BFSFringe(), 
				  DFS_OPTION   : DFSFringe(), 
				  ASTAR_OPTION : AStarFringe()}


def parse_string_int_lst(int_str):
	return [int(x) for x in int_str.split(',')]

def get_arguments():
	if (len(sys.argv) < 3):
		print 'usage: python %s <method> <board>' % sys.argv[0]
		sys.exit(1)
	return sys.argv[1], parse_string_int_lst(sys.argv[2])

def is_perfect_square(number):
	closest_root = int(sqrt(number))
	return number == (closest_root * closest_root)

def get_board_size(board_state):
	if not is_perfect_square(len(board_state)):
		print 'Error: invalid board size: %d. The size of the board must be a perfect square' % (len(board_state))
		sys.exit(1)
	return sqrt(len(board_state))

def validate_board (board_state):
	board_set = set(board_state)
	for i in range(0, len(board_state)):
		if i not in board_set:
			print "Error: invalid board %s provided. Make sure the board contains all numbers from 0 to %d" % (str(board_state), len(board_state) - 1)
			sys.exit(1)


def get_fringe(method):
	if method not in FRINGE_OPTIONS:
		print "Error: invalid method provided, valid methods are %s" % (FRINGE_OPTIONS.keys())
		sys.exit(1)

	return FRINGE_OPTIONS[method]


def get_initial_board(method, board_state):
	board_size = get_board_size(board_state)
	validate_board(board_state)

	if (method == BFS_OPTION or method == DFS_OPTION):
		return Board(board_state, None, 0, 0, board_size, None)
	elif (method == ASTAR_OPTION):
		return AStarBoard(board_state, None, 0, 0, board_size, None)
	else:
		print "Error: invalid method provided, valid methods are %s" % (FRINGE_OPTIONS.keys())
		sys.exit(1)

def get_neighbor_boards(board, visited_set):
	neighbor_boards = board.get_next_states()
	non_visited_boards = []
	max_depth = 0

	for b in neighbor_boards:
		if b not in visited_set:
			max_depth = max(max_depth, b.depth)
			non_visited_boards.append(b)

	return max_depth, non_visited_boards

def solve_puzzle(fringe, initial_board):
	fringe.add_boards([initial_board])
	visited_boards = set()

	visited_boards.add(initial_board)
	
	solved_board = None
	max_depth = 0
	num_boards_expanded = 0

	start_mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

	delta_mem = 0
	max_memory = 0

	while fringe.get_size() > 0 and solved_board == None:
		curr_board = fringe.get_next_board()
		max_depth = max(max_depth, curr_board.depth)
		visited_boards.add(curr_board)

		delta_mem = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) - start_mem
		if delta_mem > max_memory:
			max_memory = delta_mem

		if (curr_board.is_solved()):
			solved_board = curr_board
			break

		num_boards_expanded += 1
		neigbor_max_depth, neighbor_boards = get_neighbor_boards(curr_board, visited_boards)
		max_depth = max(neigbor_max_depth, max_depth)

		fringe.add_boards(neighbor_boards)

	if (solved_board != None):
		return (solved_board, num_boards_expanded, max_depth, max_memory / 1000.0)

	return None

def get_path_goal(solved_board):
	path = deque()
	curr_board = solved_board

	while(curr_board.direction != None):
		path.appendleft("\'%s\'" % curr_board.direction)
		curr_board = curr_board.parent_board

	return '[%s]' % (', '.join(path))

def write_results_to_output_file(solution, run_time):
	solved_board, num_boards_expanded, max_depth, max_memory = solution
	output_file = open(OUTPUT_FILE_NAME, 'w')

	output_file.write("path_to_goal: %s\n" % (get_path_goal(solved_board)))
	output_file.write("cost_of_path: %d\n" % (solved_board.cost))
	output_file.write("nodes_expanded: %d\n" % (num_boards_expanded))
	output_file.write("search_depth: %d\n" % (solved_board.depth))
	output_file.write("max_search_depth: %d\n" % (max_depth))
	output_file.write("running_time: %f\n" % run_time)
	output_file.write("max_ram_usage: %f" % (max_memory))

	output_file.close()

if __name__ == '__main__':
	start_time = time.time()

	method, init_board_state = get_arguments()
	fringe = get_fringe(method)
	initial_board = get_initial_board(method, init_board_state)
	solution = solve_puzzle(fringe, initial_board)

	end_time = time.time()

	if solution == None:
		print "Error: No solution found for board %s" % (str(initial_board))

	write_results_to_output_file(solution, end_time - start_time)
	