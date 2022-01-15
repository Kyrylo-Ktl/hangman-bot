from aiogram.dispatcher.filters.state import State, StatesGroup


class GuessingState(StatesGroup):
    letter = State()
    word = State()
