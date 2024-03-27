 # Problem Set 4C
# Name: Abayo Joseph Desire
# Collaborators: Lily(Mentor)
# Time Spent: x:xx
# Late Days Used: x

import json
from ps4b import PlaintextMessage, EncryptedMessage # Importing your work from Part B

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing
    the list of words to load

    Returns: a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    # inFile: file
    with open(file_name, 'r') as inFile:
        # wordlist: list of strings
        wordlist = []
        for line in inFile:
            wordlist.extend([word.lower() for word in line.split(' ')])
        return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.

    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"").lower()
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story[:-1]

def get_story_pads():
    """
    Returns: pads used to encrypt story.
    """
    with open('pads.txt') as json_file:
        return json.load(json_file)

WORDLIST_FILENAME = 'words.txt'
### END HELPER CODE ###

def decrypt_message_try_pads(ciphertext, pads):
    '''
    Given a ciphertext and a list of possible pads used to create it,
    find the pad used to create the ciphertext

    We will consider the pad used to create the ciphertext as the pad
    that results in a plaintext with the most valid English words

    ciphertext (EncryptedMessage): The ciphertext
    pads (list of lists of ints): A list of pads which might
        have been used to encrypt the ciphertext

    Returns: (PlaintextMessage) A message with the decrypted ciphertext and the best pad
    '''
    valid_pad=[]
    max_valid_words=0
    for item in pads:
        temp_plaintext = ciphertext.decrypt_message(item).get_text()
        plaintext_list=temp_plaintext.split()
        num_words=0
        for text in plaintext_list:
            if is_word(load_words(WORDLIST_FILENAME), text) == True:
                num_words +=1
        if num_words > max_valid_words:
            valid_pad=item
            max_valid_words = num_words
    if max_valid_words ==0:
        return ciphertext.decrypt_message(pads[-1])
    return ciphertext.decrypt_message(valid_pad)


def decode_story():
    '''
    Write your code here to decode Bob's story using a list of possible pads
    Hint: use the helper functions get_story_string and get_story_pads and your EncryptedMessage class.

    Returns: (string) the decoded story

    '''
    return decrypt_message_try_pads(EncryptedMessage(get_story_string()), get_story_pads())

if __name__ == '__main__':
    # Uncomment these lines to try running decode_story()
    story = decode_story()
    print("Decoded story: ", story)

    # This test is checking encoding a lowercase string with punctuation in it.
    # plaintext = PlaintextMessage('hello! ', [2, 0, 1, 4, 3, 36])
    # print('Expected Output: jemprE')
    # print('Actual Output:', plaintext.get_ciphertext())

    # This test is checking capital letters
    plaintext_1 = PlaintextMessage('Desire', [0, -1, 7, 6, 5, -10])
    print('Expected Output: Ddzow[')
    print('Actual Output:', plaintext_1.get_ciphertext())

    # This test is checking special characters
    plaintext_2 = PlaintextMessage('**yu m_', [4, -12, 5, 9, -2, 4, 0])
    print('Expected Output: .}~~}q_')
    print('Actual Output:', plaintext_2.get_ciphertext())

    # This test is checking decoding a lowercase string with punctuation in it.
    # encrypted = EncryptedMessage('jemprE')
    # print('Expected Output:', 'hello!')
    # print('Actual Output:', encrypted.decrypt_message([2, 0, 1, 4, 3, 36]).get_text())

    # This test is checking uppercase and special chacters
    encrypted_1 = EncryptedMessage('Y2O-T')
    print('Expected Output:', 'M.I.T')
    print('Actual Output:', encrypted_1.decrypt_message([12, 4, 6, -1, 0]).get_text())

    # This test is checking characters when applied shift exceed ASCII numbers limit
    encrypted_2 = EncryptedMessage('iLFSni#m! ')
    print('Expected Output:', 'blackboard')
    print('Actual Output:', encrypted_2.decrypt_message([7, -32, -27, -16, 3, 7, 19, 12, 14, 27]).get_text())
