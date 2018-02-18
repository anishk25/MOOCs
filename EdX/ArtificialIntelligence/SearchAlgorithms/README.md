# Search Algorithms (Project 1)

This program solves an N puzzle board using various algorithms. The three algorithms that the program current supports include the following:
1. Depth first search
2. Breadth first search
3. A* search

To run the program you will need atleast python 2.7 installed on your machine. To run the program do the following in the terminal

## Running the program
python driver.py <algorithm> <board>

The three algorithm types are "bfs", "dfs" and "ast" (remove quotation marks when running program in the terminal). Here is an example command that solves a board using ast

python driver.py ast 0,8,7,6,5,4,3,2,1

## Input requirements

Here are the requirements of the list that is provided to the program. N denotes the size of the list given
1. N must be greater than 1
2. Must contain all numbers from 0 to N - 1
3. 0 denotes an empty space
4. N must be perfect square (for ex. 4, 9, 25)

If the conditions above are not met then the program will be immediately halted with an error.

The list provided in the program is converted to a board of size sqrt(N) x sqrt(N). For example the board 1,2,5,3,4,0,6,7,8 is converted to the following:

1 2 5
3 4 0
6 7 8

As can be seen from the example every block of size sqrt(N) becomes a new row in the board.

## Program output
The program outputs the following information in stdout after its done running: 
- path_to_goal: the sequence of moves taken to reach the goal
- cost_of_path: the number of moves taken to reach the goal
- nodes_expanded: the number of nodes that have been expanded
- search_depth: the depth within the search tree when the goal node is found
- max_search_depth:  the maximum depth of the search tree in the lifetime of the algorithm
- running_time: the total running time of the search instance, reported in seconds
- max_ram_usage: the maximum RAM usage in the lifetime of the process as measured by the ru_maxrss attribute in the 	resource module, reported in megabytes

For example:

python driver.py bfs 1,2,5,3,4,0,6,7,8

Output:

path_to_goal: ['Up', 'Left', 'Left']
cost_of_path: 3
nodes_expanded: 10
search_depth: 3
max_search_depth: 4
running_time: 0.00188088
max_ram_usage: 0.07812500






