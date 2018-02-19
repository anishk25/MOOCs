import abc

'''
Abstract class representing a fringe
'''
class Fringe:
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def add_boards(self, boards):
		return

	@abc.abstractmethod
	def get_next_board(self):
		return

	def get_size(self):
		return
