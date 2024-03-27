"""
6.101 Lab 3:
Bacon Number
"""

#!/usr/bin/env python3

import pickle

# NO ADDITIONAL IMPORTS ALLOWED!


def transform_data(raw_data):
    """
    Represent transformed_data as a dictionary mapping actors to fellow actors in a set.
    """
    # List of two dictionaries:
    # - The first connects actors to fellow actors
    # - The second connects film to actors who acted in it
    actors = [{}, {}]

    for actor_1, actor_2, film in raw_data:
        # The first dectionary
        try:
            actors[0][actor_1].add(actor_2)
        except KeyError:
            actors[0][actor_1] = {actor_1, actor_2}
        try:
            actors[0][actor_2].add(actor_1)
        except KeyError:
            actors[0][actor_2] = {actor_2, actor_1}

        # The second dictionary
        try:
            actors[1][film].add(actor_1)
            actors[1][film].add(actor_2)
        except KeyError:
            actors[1][film] = {actor_1, actor_2}
    return actors


def acted_together(transformed_data, actor_id_1, actor_id_2):
    """
    Given two actors' ids, return True if they both acted in a same movie.
    Return False otherwise.Every actor is considered to have acted with
    themselves of course.
    """
    return actor_id_2 in transformed_data[0][actor_id_1]


def actors_with_bacon_number(transformed_data, n):
    """
    Return a set of a actors' ids whose bacon number is n.
    """
    visited_actors = set()  # Visisted actors should not be visited again
    actors_with_n_bacon = {
        4724,
    }
    actors_with_n_1_bacon = set()
    if n > 2 * len(transformed_data[0]):
        return set()
    for _ in range(n):
        for actor in actors_with_n_bacon:
            if actor not in visited_actors:
                visited_actors.add(actor)
                # Only add the actors not previously visited
                actors_with_n_1_bacon = (
                    actors_with_n_1_bacon.union(transformed_data[0][actor])
                    - visited_actors
                )

        actors_with_n_bacon = actors_with_n_1_bacon
        actors_with_n_1_bacon = set()

    return actors_with_n_bacon


def bacon_path(transformed_data, actor_id):
    """
    Returns a path connecting the actor with actor_id to
    Bacon with id: 4724
    """
    return actor_to_actor_path(transformed_data, 4724, actor_id)


def actor_to_actor_path(transformed_data, actor_id_1, actor_id_2):
    """Returns a path from actor_id_1 to actor_id_2"""

    def goal_test_function(actor):
        return actor == actor_id_2

    return actor_path(transformed_data, actor_id_1, goal_test_function)


def actor_path(transformed_data, actor_id_1, goal_test_function):
    """Returns a path from actor_id_1 to another actor returned
    from the get_test_function"""
    paths = [[actor_id_1]]
    visited_actors = set()

    if goal_test_function(actor_id_1):
        return [actor_id_1]  # If the actor_id is bacon
    while paths:
        current_path = paths.pop(0)  # Keep the deleted path
        current_connections = transformed_data[0][current_path[-1]]
        for (
            actor
        ) in current_connections:  # Loop through actors connected to the current actor
            if goal_test_function(actor):
                return current_path + [actor]
            if actor not in visited_actors:
                paths.append(current_path + [actor])
                visited_actors.add(actor)
    return None


def actors_connecting_films(transformed_data, film1, film2):
    """Returns a path of actors connecting two films."""

    def is_actor_in_film(actor):
        """Returns True if the passed-in actor acted in film_2."""
        return actor in transformed_data[1][film2]

    film_paths = []
    for actor in transformed_data[1][film1]:
        film_paths.append(actor_path(transformed_data, actor, is_actor_in_film))
    film_paths.sort(key=len)
    return film_paths[0]


if __name__ == "__main__":
    with open("resources/movies.pickle", "rb") as f:
        smalldb = pickle.load(f)

        # Print smalldb
        # print(smalldb)

        # Print actor id
        # print(smalldb["Sven Batinic"])

        # Print path between two id
        # print(actor_to_actor_path(transform_data(smalldb), 32, 1338716))

        # Actors with n bacon
        # print(actors_with_bacon_number(transform_data(smalldb), 4))

        # Films id connecting two actors
        # ans = []
        # transformed_data = transform_data(smalldb)[1]
        # for (film, actors) in transformed_data.items():
        #     if {1338712, 1338716}.intersection(actors) == {1338712, 1338716}:
        #         ans.append(film)
        # print(ans)

        # Film name given it's id
        # for (name, id) in smalldb.items():
        #     if id == 295215:
        #         print(name)

    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    pass
