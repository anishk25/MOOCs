from board import Board
from astar_board import AStarBoard
from math import sqrt
from dfs_fringe import DFSFringe
from bfs_fringe import BFSFringe
from astar_fringe import AStarFringe
import sys


BFS_OPTION = 'bfs'
DFS_OPTION = 'dfs'
ASTAR_OPTION = 'ast'

FRINGE_OPTIONS = {BFS_OPTION : BFSFringe(), DFS_OPTION : DFSFringe(), ASTAR_OPTION : }


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

def get_fringe(method):
	if method in FRINGE_OPTIONS:
		return FRINGE_OPTIONS[method]
	else
		print "Error: invalid method provided, valid methods are %s" % (FRINGE_OPTIONS.keys())

def get_initial_board(method, board_state):
	if (method == BFS_OPTION or method == DFS_OPTION):
		return Board(board_state, [], 0, 0, )

if __name__ == '__main__':
	method, init_board_state = get_arguments()
 	


	

	
	