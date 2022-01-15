from random import choice

from config import LIVES_COUNT, MASK_SYMBOL, MAX_WORD_LEN, MIN_WORD_LEN
from hangman.word_generator import ALPHABET, get_random_word


class Hangman:
    ALPHABET = ALPHABET
    MASK = MASK_SYMBOL

    def __init__(self, lives: int = LIVES_COUNT):
        self.word = get_random_word(MIN_WORD_LEN, MAX_WORD_LEN)
        self.used = set()
        self.lives = lives

    @property
    def mask(self):
        return [ltr if ltr in self.used else self.MASK for ltr in self.word]

    def is_successful_guess(self, ltr: str) -> bool:
        self.used.add(ltr)
        if ltr not in self.word:
            self.lives -= 1
            return False
        return True

    def get_letter_not_in_word_hint(self) -> str:
        incorrect_letters = list(set(self.ALPHABET) - self.used)
        return choice(incorrect_letters)

    def get_letter_in_word_hint(self) -> str:
        correct_letters = list(set(self.word) - self.used)
        return choice(correct_letters)

    def is_loose(self):
        return self.lives < 1

    def is_win(self):
        return not set(self.word) - self.used

    def is_game_finished(self):
        return self.is_win() or self.is_loose()
