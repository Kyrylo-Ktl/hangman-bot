from random import choice

from config import DICTIONARY_FILE


with open(DICTIONARY_FILE, 'rt', encoding='utf8') as dictionary:
    content = dictionary.read()
    WORDS = [word for word in content.split('\n')]
    ALPHABET = set(content) - {'\n'}


def get_random_word(min_len: int = 0, max_len: int = 100) -> str:
    while not (min_len <= len(word := choice(WORDS)) <= max_len):
        ...
    return word
