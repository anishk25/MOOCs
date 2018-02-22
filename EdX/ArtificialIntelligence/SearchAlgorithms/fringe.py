import abc

'''
Abstract class representing a fringe
'''
class Fringe:
	__metaclass__ = abc.ABCMeta

	def __init__(self):
		self._fringe_set = set()


	@abc.abstractmethod
	def add_boards(self, boards):
		return

	@abc.abstractmethod
	def get_next_board(self):
		return
		
	@abc.abstractmethod
	def get_size(self):
		return
