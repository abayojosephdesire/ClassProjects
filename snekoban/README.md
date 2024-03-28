# Snekoban

In this project, we implemented a version of a popular game called Sokoban. The original game involves moving a person around a virtual warehouse floor, pushing boxes onto target locations, until each target is covered with a box. In our version ("Snekoban"), rather than a warehouse worker, the player controls a little python (), and the goal is to push computers () around a world surrounded by walls () until every target () is covered with a computer.
We started by implementing the rules of the game (which are described in much more detail below), and then we wrote an additional program that solves Sokoban puzzles, producing as output a sequence of moves that takes us from a starting configuration to one that solves the puzzle.

# 1. Game Rules
This section talks through the various components that make up the game, as well as the rules of the game. It may be worth reading through all of section.
Meanwhile, the server and our test cases uses a canonical representation of the game. Eventually, we had to write a function that converts to and from this canonical representation and our internal representation of the game.

# 1.1. Board
The game board is an m*n grid, where m and n are the numbers of rows and columns, respectively. The location of each cell at row i and column j can be represented as a Python tuple, (i, j). Each cell of the board may contain zero, one, or multiple objects. In a valid puzzle, there will always be the same number of computers as targets.
The canonical representation represents the board as a Python list of lists of lists of strings, where the first two layers of lists are for rows and columns, and the third layer of list is to list all the objects in each location.

# 1.2. Objects
There are four possible different kinds of objects in the game: the player (), computers (), walls (), and targets ().

# 1.2.1. The Player 
The player of the game controls a python (). The player can move around the board by pressing the arrow keys. Pressing an arrow key will attempt to move the player in the given direction, subject to some interactions described below.

# 1.2.2. Walls 
Walls () are stationary objects that prevent movement. Any object attempting to move to a location occupied by a wall instead remains in its original position.
In all of the provided puzzles, the player starts in an area that is completely enclosed by walls. Your code does not need to handle other cases.

# 1.2.3. Computers 
Computers () are objects that the player can push around the board. If the player () attempts to move to a location containing a computer, the computer should be "pushed" in the same direction in which the player was moving, unless doing so would move the computer in question onto a wall or another computer (in which case all objects, including the player, remain in their original positions instead).

# 1.2.4. Targets 
Targets () represent locations to which we would like to push computers (). Targets are always stationary. The player or a computer can move onto targets.
The goal of the game is to push computers () onto targets (). The game is won when every spot containing a target also contains a computer. However, if there are no targets, the player does not automatically win; instead, this makes the game unwinnable.
It is possible that some targets already begin in the same spots as computers, but in some cases, the solution may involve moving that computer away, either temporarily or permanently.

# 1.3. Interface
To the pass test cases that we provide, lab.py file should implement the following functions, which will provide an interface to the game without restricting your choice of internal representation:
"make_new_game" takes in the canonical representation of the game and returns your internal representation of the game state.
"step_game" takes in the player's action and a game representation (as returned from make_new_game) and returns a new game in that same representation, updated according to one step of the game (without modifying the object that was passed in). The possible actions that a player can take are "up", "down", "right", and "left".
"victory_check" takes in a game (in your chosen representation) and returns a Boolean: True if the game has been won and False otherwise. A game with no computers or targets should never satisfy the victory condition.
"dump_game" takes in a game representation (as returned from make_new_game) and converts it back into the canonical representation (which is used by the test cases and the GUI).

# 1.4. GUI
The functions above provide the programmatic interface to the game, and they should be sufficient for small-scale testing and debugging (for example, by creating a new game, stepping it multiple times, and then printing the results to see if they match your expectations), and this same interface is used by our test cases.
That said, it's not very fun to play the game that way, so we have also provided a way to play the game in the browser (using your code). To do so, run the following command in your terminal (where /path/to/server.py refers to the location of server.py in the code distribution for this lab):
>>> python3/path/to/server.py
After doing so, if you navigate to http://localhost:6101 in your web browser, you should be able to play the game!
There are several different levels to play through, all of which were designed by David W. Skinner. The particular levels we include are from the "Microban," "Mas Microban," "Sasquatch," and "Mas Sasquatch" puzzle sets. These same puzzles also act as the starting points for many of our test cases.
