"""
6.1010 Lab 4:
Snekoban Game
"""

import json
import typing

# NO ADDITIONAL IMPORTS!


direction_vector = {
    "up": (-1, 0),
    "down": (+1, 0),
    "left": (0, -1),
    "right": (0, +1),
}


def make_new_game(level_description):
    """
    Given a description of a game state, create and return a game
    representation of your choice.

    The given description is a list of lists of lists of strs, representing the
    locations of the objects on the board (as described in the lab writeup).

    For example, a valid level_description is:

    [
        [[], ['wall'], ['computer']],
        [['target', 'player'], ['computer'], ['target']],
    ]

    The exact choice of representation is up to you; but note that what you
    return will be used as input to the other functions.

    ------------------------------
    Our representation for the board
    'player':0, 'target':1, 'computer':2, 'wall':3

    {
        "targets" : {(2,3), (1,2)},
        "walls" : {(1,1), (2,1)},
        "comps" : {(4,3),(2,2)},
        "player" : (2,2),
    }
    """
    # Boards representation
    board_representation = {
        "targets": set(),
        "walls": set(),
        "comps": set(),
        "dimensions": (len(level_description), len(level_description[0])),
        "player": (None, None),
    }
    board_height = len(level_description)
    board_width = len(level_description[0])

    # Loop through the entire bord, neglecting empty lists
    # Update the board_representation
    for row in range(board_height):
        for col in range(board_width):
            cell_repr = level_description[row][col]
            if "wall" in cell_repr:
                board_representation["walls"].add((row, col))
            elif "target" in cell_repr:
                board_representation["targets"].add((row, col))
            if "computer" in cell_repr:
                board_representation["comps"].add((row, col))
            if "player" in cell_repr:
                board_representation["player"] = (row, col)

    return board_representation


def victory_check(game):
    """
    Given a game representation (of the form returned from make_new_game),
    return a Boolean: True if the given game satisfies the victory condition,
    and False otherwise.

    ------------------------------
    Returns true if all computers are placed in right targets
    """
    # Game with no computers/targets should never pass this test
    if game["targets"] and game["comps"]:
        return game["targets"] == game["comps"]
    return False


def step_game(game, direction):
    """
    Given a game representation (of the form returned from make_new_game),
    return a new game representation (of that same form), representing the
    updated game after running one step of the game.  The user's input is given
    by direction, which is one of the following:
        {'up', 'down', 'left', 'right'}.

    This function should not mutate its input.
    """
    # Comp positions
    comps_pos = set(game["comps"])
    player_pos = game["player"][:]

    next_player_pos = (
        player_pos[0] + direction_vector[direction][0],
        player_pos[1] + direction_vector[direction][1],
    )
    next_next_pos = (
        next_player_pos[0] + direction_vector[direction][0],
        next_player_pos[1] + direction_vector[direction][1],
    )

    # Handles the constraints: walls
    if next_player_pos not in game["walls"]:
        if next_player_pos not in game["walls"].union(game["comps"]):
            player_pos = next_player_pos
        elif next_player_pos in game["comps"] and next_next_pos not in game[
            "comps"
        ].union(game["walls"]):
            comps_pos.remove(next_player_pos)
            comps_pos.add(next_next_pos)
            player_pos = next_player_pos

    return {
        "targets": game["targets"],
        "walls": game["walls"],
        "player": player_pos,
        "comps": comps_pos,
        "dimensions": game["dimensions"],
    }


def dump_game(game):
    """
    Given a game representation (of the form returned from make_new_game),
    convert it back into a level description that would be a suitable input to
    make_new_game (a list of lists of lists of strings).

    This function is used by the GUI and the tests to see what your game
    implementation has done, and it can also serve as a rudimentary way to
    print out the current state of your game for testing and debugging on your
    own.
    """
    # Default board representation
    board_repr = [
        [[] for _ in range(game["dimensions"][1])] for _ in range(game["dimensions"][0])
    ]

    # Place walls, targets, computers, and player on the board
    for row, col in game["targets"]:
        board_repr[row][col].append("target")
    for row, col in game["comps"]:
        board_repr[row][col].append("computer")
    for row, col in game["walls"]:
        board_repr[row][col].append("wall")
    board_repr[game["player"][0]][game["player"][1]].append("player")

    return board_repr


def solve_puzzle(game):
    """
    Given a game representation (of the form returned from make_new_game), find
    a solution.

    Return a list of strings representing the shortest sequence of moves ("up",
    "down", "left", and "right") needed to reach the victory condition.

    If the given level cannot be solved, return None.
    """
    if victory_check(game):
        return []  # If the game is won already

    # Board representation --- tuple sorting would be helpful in search
    board = (game["player"], tuple(sorted(game["comps"])))
    visited = {board}
    moves = [
        {
            "moves": [],
            "comps": set(game["comps"]),
            "player": game["player"][:],
        },
    ]

    while moves:
        curr_move = moves.pop(0)

        # Loop through the four possible directions
        for dir_name in direction_vector:
            next_game = step_game(
                {
                    "targets": game["targets"],
                    "walls": game["walls"],
                    "player": curr_move["player"],
                    "comps": curr_move["comps"],
                    "dimensions": game["dimensions"],
                },
                dir_name,
            )

            if victory_check(next_game):  # Check the victorty status
                return curr_move["moves"] + [dir_name]

            curr_board = (next_game["player"], tuple(sorted(next_game["comps"])))

            # Updated visited and moves
            if curr_board not in visited:
                visited.add(curr_board)
                moves.append(
                    {
                        "moves": curr_move["moves"] + [dir_name],
                        "comps": set(next_game["comps"]),
                        "player": next_game["player"][:],
                    }
                )

    return None


if __name__ == "__main__":
    pass

    # Test make_new_game()
    # level_description = [
    #     [[], ['wall'], ['computer']],
    #     [['target', 'player'], ['computer'], ['target']],
    # ]
    # print("Results: ", make_new_game(level_description))

    # Test dump_game()
    # print("Results: ", dump_game(make_new_game(level_description)))

    # Test solve_puzzle()
    # level = [
    #     [["wall"], ["wall"], ["wall"], ["wall"], [], []],
    #     [["wall"], [], ["target"], ["wall"], [], []],
    #     [["wall"], [], [], ["wall"], ["wall"], ["wall"]],
    #     [["wall"], ["target", "computer"], ["player"], [], [], ["wall"]],
    #     [["wall"], [], [], ["computer"], [], ["wall"]],
    #     [["wall"], [], [], ["wall"], ["wall"], ["wall"]],
    #     [["wall"], ["wall"], ["wall"], ["wall"], [], []],
    # ]

    # board = make_new_game(level)
    # print(solve_puzzle(board))
