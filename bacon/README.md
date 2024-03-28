# Bacon

# Introduction
Have you heard of Six Degrees of Separation? This simple theory states that at most 6 people separate you from any other person in the world. Hollywood has its own version: Kevin Bacon is the center of the universe (not really, but let's let him feel good about himself). Every actor who has acted with Kevin Bacon in a movie is assigned a "Bacon number" of 1, every actor who acted with someone who acted with Kevin Bacon is given a "Bacon number" of 2, and so on. (What Bacon number does Kevin Bacon have? Think about it for a second.)
Note that if George Clooney acts in a movie with Julia Roberts, who has acted with Kevin Bacon in a different film, George has a Bacon number of 2 through this relationship. If George himself has also acted in a movie with Kevin, however, then his Bacon number is 1, and the connection through Julia is irrelevant. We define the notion of a "Bacon number" to be the smallest number of films separating a given actor (or actress) from Kevin Bacon.
In this project, we explored the notion of the Bacon number. We had an ambitious database of approximately 37,000 actors and 10,000 films so that we may look up for favorites. Did Julia Roberts and Kevin Bacon act in the same movie? And what does Robert De Niro have to do with Frozen? Let's find out!

# 1.1. The Film Database
We've mined a large database of actors and films from IMDB via the www.themoviedb.org API. We present this data as a list of records (3-element tuples), each of the form (actor_id_1, actor_id_2, film_id), which tells us that actor_id_2 acted with actor_id_1 in a film denoted by film_id.
Keep in mind that "acts with" is a symmetric relationship. If (a1, a2, f) is in the database, it is true both that a1 acted with a2 and that a2 acted with a1, even if (a2, a1, f) is not explicitly represented in the database.
However, these relationships do not necessarily exhibit the transitive property. That is, if (a1, a2, f) and (a2, a3, f) are in the database, it is not necessarily true that a1 and a3 have acted together (unless (a1, a3, f) or (a3, a1, f) is in the database explicitly). One way to think about this is that "act together" might mean "appear on-screen together." So a1 and a3 may be in the same film, and each appear separately on-screen with a2 at some point in the film, but a1 and a3 are never on-screen together at the same time.
We stored these data as pickle files. The server tests will use small.pickle and large.pickle, but we have also included a tiny.pickle that we used to write our own tests.

# 1.2. The Names Database
The functions in lab.py expect us to use integer actor IDs, but the tests we give you on this page will have actor names as inputs and outputs.
To help with this mapping, we include a file, resources/names.pickle, which contains a representation of the mapping between actor IDs and names. You can use the load function of Python's pickle module to get the data out of the file and into Python. We have included an example in the if __name__ == '__main__' section of lab.py.

# 1.3. Using the UI
We have also provided a visualization website which loads our code into a small server (server.py) and visualizes your results. To use the visualization, run python3 server.py and use your web browser navigate to localhost:6101. You will need to restart server.py in order to reload your code if you make changes.
You will be able to see actors as circular nodes (hover above the node to see the actor's name) and the movies as edges linking nodes together.
Above the graph we define three different tabs, one for each component of the project. Each tab sets up the visualization appropriate for its aspect of the project.

# 1.4. lab.py and test.py
These files are yours to edit in order to complete this project too. You should implement the main functionality of the lab in lab.py, and you are strongly encouraged to implement additional test cases (as described throughout the assignment) in test.py as you're working.

Additional comments were provided in lab.py
