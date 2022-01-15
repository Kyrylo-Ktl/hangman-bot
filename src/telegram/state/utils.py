from aiogram.dispatcher import FSMContext

from hangman.hangman import Hangman

HANGMAN_OBJ = 'hangman'


class CurrentGameHandler:
    @staticmethod
    async def init(state: FSMContext):
        await state.set_data({HANGMAN_OBJ: Hangman()})

    @staticmethod
    async def get(state: FSMContext) -> Hangman:
        data = await state.get_data()
        hangman = data[HANGMAN_OBJ]
        return hangman

    @staticmethod
    async def update(state: FSMContext, hangman: Hangman):
        await state.update_data(**{HANGMAN_OBJ: hangman})
