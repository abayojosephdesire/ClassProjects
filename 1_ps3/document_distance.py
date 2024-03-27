# 6.100A Fall 2023
# Problem Set 3
# Name: Abayo Joseph Desire
# Collaborators: Lily (Mentor)

"""
Description:
    Computes the similarity between two texts using two different metrics:
    (1) shared words, and (2) term frequency-inverse document
    frequency (TF-IDF).
"""

import string
import math
import re

### DO NOT MODIFY THIS FUNCTION
def load_file(filename):
    """
    Args:
        filename: string, name of file to read
    Returns:
        string, contains file contents
    """
    # print("Loading file %s" % filename)
    inFile = open(filename, 'r')
    line = inFile.read().strip()
    for char in string.punctuation:
        line = line.replace(char, "")
    inFile.close()
    return line.lower()


### Problem 1: Prep Data ###
def prep_data(input_text):
    """
    Args:
        input_text: string representation of text from file,
                    assume the string is made of lowercase characters
    Returns:
        list representation of input_text, where each word is a different element in the list
    """
    return input_text.split()


### Problem 2: Get Frequency ###
def get_frequencies(word_list):
    """
    Args:
        word_list: list of strings, all are made of lowercase characters
    Returns:
        dictionary that maps string:int where each string
        is a word in l and the corresponding int
        is the frequency of the word in l
    """
    temp_dict={} # Dictionary holding the frequencies
    for i in word_list:
        if i in temp_dict:
            temp_dict[i] +=1
        else:
            temp_dict[i] = 1
    return temp_dict


### Problem 3: Get Words Sorted by Frequency
def get_words_sorted_by_frequency(frequencies_dict):
    """
    Args:
        frequencies_dict: dictionary that maps a word to its frequency
    Returns:
        list of words sorted by decreasing frequency with ties broken
        by alphabetical order
    """
    li_keys=[] # list holding key sorted depending on values
    li_value=sorted(frequencies_dict.values())
    max_value=max(li_value)
    for i in range(max_value+1,0,-1):
        li_temp=[]
        for key, value in frequencies_dict.items():
            if value == i:
                li_temp.append(key)
        li_temp.sort()
        li_keys.extend(li_temp)

    return li_keys



### Problem 4: Most Frequent Word(s) ###
def get_most_frequent_words(dict1, dict2):
    """
    The keys of dict1 and dict2 are all lowercase,
    you will NOT need to worry about case sensitivity.

    Args:
        dict1: frequency dictionary for one text
        dict2: frequency dictionary for another text
    Returns:
        list of the most frequent word(s) in the input dictionaries

    The most frequent word:
        * is based on the combined word frequencies across both dictionaries.
          If a word occurs in both dictionaries, consider the sum the
          frequencies as the combined word frequency.
        * need not be in both dictionaries, i.e it can be exclusively in
          dict1, dict2, or shared by dict1 and dict2.
    If multiple words are tied (i.e. share the same highest frequency),
    return an alphabetically ordered list of all these words.
    """
    new_dict={}
    for key, value in dict1.items(): # Loop through all words of dict1 and add values
        if key in new_dict:
            new_dict[key] += value
        else:
            new_dict[key] = value
    for key, value in dict2.items(): # Loop through all words of dict2 and add values
        if key in new_dict:
            new_dict[key] += value
        else:
            new_dict[key] = value
    new_dict_val=[freq for freq in new_dict.values()] # List of all values/frequencies
    max_freq=max(new_dict_val)
    res_list=[]
    for key, value in new_dict.items():
        if value == max_freq: # Just add keys with the maximum value
            res_list.append(key)
    res_list.sort()
    return res_list


### Problem 5: Similarity ###
def calculate_similarity_score(dict1, dict2):
    """
    The keys of dict1 and dict2 are all lowercase,
    you will NOT need to worry about case sensitivity.

    Args:
        dict1: frequency dictionary of words of text1
        dict2: frequency dictionary of words of text2
    Returns:
        float, a number between 0 and 1, inclusive
        representing how similar the words/texts are to each other

        The difference in words/text frequencies = DIFF sums "frequencies"
        over all unique elements from dict1 and dict2 combined
        based on which of these three scenarios applies:
        * If an element occurs in dict1 and dict2 then
          get the difference in frequencies
        * If an element occurs only in dict1 then take the
          frequency from dict1
        * If an element occurs only in dict2 then take the
          frequency from dict2
         The total frequencies = ALL is calculated by summing
         all frequencies in both dict1 and dict2.
        Return 1-(DIFF/ALL) rounded to 2 decimal places
    """
    unique_list=[]
    for key in dict1: # Add unique keys in the list
        if key not in unique_list:
            unique_list.append(key)
    for key in dict2: # Add unique keys inm the list
        if key not in unique_list:
            unique_list.append(key)
    DIFF=0
    ALL=0
    for item in unique_list: # Compute DIFF and ALL for each word
        if item in dict1 and item in dict2:
            DIFF += abs(dict1[item] - dict2[item])
            ALL += (dict1[item] + dict2[item])
        elif item in dict1:
            DIFF += dict1[item]
            ALL += dict1[item]
        else:
            DIFF += dict2[item]
            ALL += dict2[item]
    score = 1 - (DIFF/ALL)
    score_round = round(score, 2)
    return score_round


### Problem 6: Finding TF-IDF ###
def get_tf(text_file):
    """
    Args:
        text_file: name of file in the form of a string
    Returns:
        a dictionary mapping each word to its TF

    * TF is calculated as TF(i) = (number times word *i* appears
        in the document) / (total number of words in the document)
    * Think about how we can use get_frequencies from earlier
    """
    words_str=load_file(text_file)
    words_lst=prep_data(words_str)
    words_tot=len(words_lst) # Number of words in the file
    words_dict=get_frequencies(words_lst) # Returns a dictionary of words and frequencies
    for key, value in words_dict.items(): # Loop compute TF
        words_dict[key]=value/words_tot
    return words_dict

def get_idf(text_files):
    """
    Args:
        text_files: list of names of files, where each file name is a string
    Returns:
       a dictionary mapping each word to its IDF

    * IDF is calculated as IDF(i) = log_10(total number of documents / number of
    documents with word *i* in it), where log_10 is log base 10 and can be called
    with math.log10()

    """
    final_dict={} # Final dictionary with  IDF values.
    files_tot=len(text_files) # Number of files in the parameter
    for item in text_files: # Loop through all files
        words_str = load_file(item)
        words_lst=prep_data(words_str)
        words_uniq=[] # Unique words
        for item in words_lst: # Add unique values in the list
            if item not in words_uniq:
                words_uniq.append(item)
        for word in words_uniq: # Add unique keys in final dictionary
            if word in final_dict:
                final_dict[word] +=1
            else:
                final_dict[word] =1
    for key, value in final_dict.items(): # Compute IDF for each value
        final_dict[key] = math.log10(files_tot/value)
    return final_dict


def get_tfidf(text_file, text_files):
    """
    Args:
        text_file: name of file in the form of a string (used to calculate TF)
        text_files: list of names of files, where each file name is a string
        (used to calculate IDF)
    Returns:
       a sorted list of tuples (in increasing TF-IDF score), where each tuple is
       of the form (word, TF-IDF). In case of words with the same TF-IDF, the
       words should be sorted in increasing alphabetical order.

    * TF-IDF(i) = TF(i) * IDF(i)
    """
    words_tf=get_tf(text_file) # Returns a dictionary with words and their TF
    words_idf=get_idf(text_files) # Returns a dictionary with words and their IDF
    final_dict={}
    for key in words_tf:
        final_val = words_tf[key] * words_idf[key] # Computer TF-IDF
        final_dict[key] = final_val

    final_dict_copy=final_dict.copy() # Copy of the above computed dictionary
    final_lst=[] # Final list to be returned
    while len(final_dict_copy) != 0: # Whever the final_dict_copy is not empty
        min_val=min(final_dict_copy.values()) # Minimum value in the dictionary
        temp_lst=[] # Temporary list to sort items with same value
        for key, value in final_dict.items():
            if value == min_val:
                temp_lst.append((key, value)) # Add tuple to temp_lst
                del final_dict_copy[key] # Delete dictionary item added to the temp_lst
        temp_lst.sort() # Sort items with same value
        final_lst += temp_lst # Append the list to the final_lst
    return final_lst

if __name__ == "__main__":
    pass
    # ##Uncomment the following lines to test your implementation
    # Tests Problem 1: Prep Data
    test_directory = "tests/student_tests/"
    hello_world, hello_friend = load_file(test_directory + 'hello_world.txt'), load_file(test_directory + 'hello_friends.txt')
    world, friend = prep_data(hello_world), prep_data(hello_friend)
    print(world) ## should print ['hello', 'world', 'hello', 'there']
    print(friend) ## should print ['hello', 'friends']

    ## Tests Problem 2: Get Frequencies
    world_word_freq = get_frequencies(world)
    friend_word_freq = get_frequencies(friend)
    print(world_word_freq) ## should print {'hello': 2, 'world': 1, 'there': 1}
    print(friend_word_freq) ## should print {'hello': 1, 'friends': 1}

    # ## Tests Problem 3: Get Words Sorted by Frequency
    world_words_sorted_by_freq = get_words_sorted_by_frequency(world_word_freq)
    friend_words_sorted_by_freq = get_words_sorted_by_frequency(friend_word_freq)
    print(world_words_sorted_by_freq) ## should print ['hello', 'there', 'world']
    print(friend_words_sorted_by_freq) ## should print ['friends', 'hello']

    ## Tests Problem 4: Most Frequent Word(s)
    freq1, freq2 = {"hello":5, "world":1}, {"hello":1, "world":5}
    most_frequent = get_most_frequent_words(freq1, freq2)
    print(most_frequent) ## should print ["hello", "world"]

    ## Tests Problem 5: Similarity
    test_directory = "tests/student_tests/"
    hello_world, hello_friend = load_file(test_directory + 'hello_world.txt'), load_file(test_directory + 'hello_friends.txt')
    world, friend = prep_data(hello_world), prep_data(hello_friend)
    world_word_freq = get_frequencies(world)
    friend_word_freq = get_frequencies(friend)
    word_similarity = calculate_similarity_score(world_word_freq, friend_word_freq)
    print(word_similarity)        # should print 0.33

    ## Tests Problem 6: Find TF-IDF
    text_file = 'tests/student_tests/hello_world.txt'
    text_files = ['tests/student_tests/hello_world.txt', 'tests/student_tests/hello_friends.txt']
    tf = get_tf(text_file)
    idf = get_idf(text_files)
    tf_idf = get_tfidf(text_file, text_files)
    print(tf) ## should print {'hello': 0.5, 'world': 0.25, 'there': 0.25}
    print(idf) ## should print {'there': 0.3010299956639812, 'world': 0.3010299956639812, 'hello': 0.0, 'friends': 0.3010299956639812}
    print(tf_idf) ## should print [('hello', 0.0), ('there', 0.0752574989159953), ('world', 0.0752574989159953)]
