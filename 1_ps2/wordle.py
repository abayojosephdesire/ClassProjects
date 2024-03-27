# Problem Set 2, wordle.py
# Name: Abayo Joseph Desire
# Collaborators: N/A
# Time spent: 180

# Wordle Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()

def check_user_input(secret_word, user_guess):
    """

    :param secret_word: a string, the word to be guessed
    :param user_guess: a string, the users guess
    :return: False if user_guess does not satisfy at least
	     one of the below conditions, True otherwise.
    1. must consist of only letters (uppercase or lowercase)
    2. must be the same length as secret_word
    3. must be a word found in words.txt
    """
# Print a warning and return False if the user_guess contains non-alphabet characters
    if len(secret_word) != len(user_guess):
        print("Oops! That word length is not correct.")
        return False
    # Print a warning and return False if the user_guess is shorter or longer than the secret_word
    elif not user_guess.isalpha():
        print("Oops! That is not a valid word.")
        return False
    # Print a warning and return False if the user_guess is not included in the wordlist
    elif user_guess.lower().strip() not in wordlist:
        print("Oops! That is not a real word.")
        return False
    # Print True because user_guess is valid
    return True

def get_guessed_feedback(secret_word, user_guess):
    """

    :param secret_word: a string, the word to be guessed
    :param user_guess: a string, a valid user guess
    :return: a string with uppercase and lowercase letters and
	     underscores, each separated by a space (e.g. 'B _ _ S u')
    """

    res=[] # A hint on form of a list of alphanumerics and underscore
    user_guess_strip = user_guess.strip()
    for i in range(len(secret_word)):
        if user_guess_strip[i] in secret_word:
            if user_guess_strip[i] == secret_word[i]:
                res.append(user_guess_strip[i].upper())
            else:
                res.append(user_guess_strip[i])
        else:
            res.append('_')
    return " ".join(res)

def get_alphabet_hint(secret_word, all_guesses):
    """
    takes in the secret word and a list of all previous guesses and returns a string of hint text
    :param secret_word: a string, the word to be guessed
    :param all_guesses: a list of all the previous valid guesses the user inputed
    :return: a string which replaces letters that were incorrect guesses with underscores and puts
	     semi-correct guesses (correct letter, incorrect place) in /x/
    """
    # we have coded this for you
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    out_list = []
    for char in alphabet:
        out_list.append(" "+char+" ")

    for guess in all_guesses:
        for i, char in enumerate(list(guess)):
            if char not in secret_word:
                out_list[alphabet.find(char)]=" _ "
            elif char != secret_word[i]:
                out_list[alphabet.find(char)] = "/"+char+"/"
            elif char == secret_word[i]:
                if secret_word.count(char) > guess.count(char):
                    out_list[alphabet.find(char)] = "/" + char + "/"
                else:
                    out_list[alphabet.find(char)] = "|" + char.upper() + "|"
    return "".join(out_list)

def wordle(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Wordle.

    * At the start of the game, let the user know how many letters the
      secret_word contains and how many guesses and warnings they start with.

    * The user should start with 6 guesses and 3 warnings

    * Before each round, you should display to the user how many guesses
      they have left.

    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a valid word!

    * The user should receive feedback immediately after each guess about
      whether their guess is valid, how closely it matches the secret_word,
      and the alphabet hint.

    * After each guess, you should display to the user the progression of
      their partially guessed words so far.

    Follows the other limitations detailed in the problem write-up.
    '''

    # Opening messages
    print("Welcome to the game Wordle!")
    print(f"I am thinking of a word that is {len(secret_word)} letters long.")
    print("You have 3 warnings remaining.")

    all_guesses=[] # Words guessed
    resp=[] # List of hints based on the user guesses
    warn=3 # Warnings
    guesses_remaining=6 # Remaining guesses
    uniq=[] # List of tested characters

    # Add uniques tested characters in the list uniq
    for i in secret_word:
        if i not in uniq:
            uniq.append(i)

    # As long as the user still has guesses...
    while guesses_remaining >= 1:
        print(f"You have {guesses_remaining} guesses left.")
        tes=input("Please guess a word: ")

        # If the word is valid
        if check_user_input(secret_word, tes):
            all_guesses.append(tes) # Add user input to the list of tested words

            # Test if the user guessed the correct word
            if tes==secret_word:
                print("Congratulations, you won!")
                print(f"You guessed the correct word in {7 - guesses_remaining} tries!")
                print(f"Your total score is {(guesses_remaining -1) * len(uniq)}.")
                break
            else:

                # Give the user some hints
                resp.append(get_guessed_feedback(secret_word, tes))

                # Print all guess hints
                for i in resp:
                    print(i)
                print("Alphabet HINT:")
                print(get_alphabet_hint(secret_word, all_guesses))

                # When all guesses are exhausted
                if guesses_remaining==1:
                    print(f"Sorry, you ran out of guesses. The word was {secret_word}.")
                    break
                else:
                    print("----------")
                    guesses_remaining -= 1

        else:
            if warn >=1:
                warn -=1
            # Warnings exhausted
            else:
                if guesses_remaining==1:
                    print(f"Sorry, you ran out of guesses. The word was {secret_word}.")
                    break
                else:
                    guesses_remaining -=1
            print(f"You have {warn} warnings remaining.")
            print("----------")


if __name__ == "__main__":
    pass

    # To test, comment out the `pass` line above and uncomment:
    # - either of the `secret_word = ...` lines below, depending on how you want to set the secret_word
    # - the `wordle(secret_word)` line to run the game

    # uncomment and change the line below to a specific word for testing
    # secret_word = "team"

    # uncomment the line below for a randomly generated word
    secret_word = choose_word(wordlist)

    wordle(secret_word)
