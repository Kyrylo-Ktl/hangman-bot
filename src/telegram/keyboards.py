from aiogram.types import ReplyKeyboardMarkup

from hangman.hangman import Hangman
from telegram.buttons import END_GAME, GUESS_WORD, HINT, NEW_GAME


def get_adaptive_size(n_items: int, min_size: int, max_size: int) -> int:
    best_size = max_size
    for size in range(max_size, min_size - 1, -1):
        if not n_items % size:
            best_size = size
            break
        if n_items % best_size < n_items % size:
            best_size = size
    return best_size


def get_start_game_keyboard() -> ReplyKeyboardMarkup:
    """Create a button for starting game"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    keyboard.add(NEW_GAME)
    return keyboard


def get_alphabet_keyboard(used_letters: set) -> ReplyKeyboardMarkup:
    """Create a keyboard with alphabet and additional buttons"""
    letters = sorted(set(Hangman.ALPHABET) - used_letters)
    best_row_width = get_adaptive_size(len(letters), 5, 8)

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=best_row_width)
    keyboard.add(*letters)
    keyboard.add(END_GAME, HINT, GUESS_WORD)
    return keyboard
