"""A Python library to check for (and clean) profanity in strings.

"""

import os
import random
import string

lines = None
words = None
_censor_chars = '@#$%!'
_censor_pool = []

_ROOT = os.path.abspath(os.path.dirname(__file__))


def get_data(path):
    return os.path.join(_ROOT, 'data', path)


def get_words():
    if not words:
        load_words()
    return words


def get_censor_char():
    """Plucks a letter out of the censor_pool. If the censor_pool is empty,
    replenishes it. This is done to ensure all censor chars are used before
    grabbing more (avoids ugly duplicates).

    """
    global _censor_pool
    if not _censor_pool:
        # censor pool is empty. fill it back up.
        _censor_pool = list(_censor_chars)
    return _censor_pool.pop(random.randrange(len(_censor_pool)))


def set_censor_characters(censor_chars):
    """Sets the pool of censor characters. Input should be a single string
    containing all the censor charcters you'd like to use.
    Example: "@#$%^"

    """
    global _censor_chars
    _censor_chars = censor_chars


def contains_profanity(input_text):
    """Checks the input_text for any profanity and returns True if it does.
    Otherwise, returns False.
    """
    return input_text != censor(input_text)


def censor(input_text, censor_chars=False):
    """ Returns the input string with profanity replaced with a random string
    of characters plucked from the censor_characters pool.

    """
    ret = set(input_text.strip().lower().translate(None, string.punctuation).split())
    bad_words = get_words()

    to_censor = ret.intersection(words)

    for word in to_censor:
        input_text = input_text.replace(word, 'cheese')

    return input_text

def load_words(wordlist=None):
    """ Loads and caches the profanity word list. Input file (if provided)
    should be a flat text file with one profanity entry per line.

    """
    global words
    if not wordlist:
        # no wordlist was provided, load the wordlist from the local store
        filename = get_data('wordlist.txt')
        f = open(filename)
        wordlist = f.readlines()
        wordlist = set([w.strip() for w in wordlist if w])
    words = wordlist
