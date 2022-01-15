from config import LIVE_SYMBOL
from hangman.hangman import Hangman
from telegram.message.messages import CORRECT_LETTER, GAME_STATE_MESSAGE, HINT, INCORRECT_LETTER, LOOSE, WIN


class MessageFormer:
    @staticmethod
    def get_hint_message(hangman: Hangman) -> str:
        message = HINT.format(
            exst_letter=hangman.get_letter_in_word_hint(),
            unex_letter=hangman.get_letter_not_in_word_hint(),
        )
        return message

    @staticmethod
    def get_try_result_message(success_try: bool) -> str:
        if success_try:
            return CORRECT_LETTER
        return INCORRECT_LETTER

    @staticmethod
    def get_game_ending_message(hangman: Hangman) -> str:
        if not hangman.is_game_finished():
            raise Exception('Game isn`t finished')

        if hangman.is_loose():
            return LOOSE.format(word=hangman.word)
        return WIN

    @staticmethod
    def get_game_state_message(hangman: Hangman) -> str:
        message = GAME_STATE_MESSAGE.format(
            word=MessageFormer._get_mask_message(hangman),
            lives=MessageFormer._get_lives_message(hangman),
        )
        return message

    @staticmethod
    def _get_mask_message(hangman: Hangman) -> str:
        return ' '.join(hangman.mask)

    @staticmethod
    def _get_lives_message(hangman: Hangman) -> str:
        return LIVE_SYMBOL * hangman.lives
