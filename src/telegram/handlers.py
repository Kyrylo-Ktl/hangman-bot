from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from config import dp
from hangman.hangman import Hangman
from telegram import buttons
from telegram.keyboards import get_alphabet_keyboard, get_start_game_keyboard
from telegram.message import messages
from telegram.message.utils import MessageFormer
from telegram.state.storage import GuessingState
from telegram.state.utils import CurrentGameHandler


@dp.message_handler(commands='start')
async def cmd_start(message: Message):
    await message.answer(messages.INITIAL, reply_markup=get_start_game_keyboard())


@dp.message_handler(lambda message: message.text != buttons.NEW_GAME)
async def process_invalid_new_game(message: Message):
    await message.answer(messages.NEW_GAME, reply_markup=get_start_game_keyboard())


@dp.message_handler(lambda message: message.text == buttons.NEW_GAME)
async def process_new_game(message: Message, state: FSMContext):
    await GuessingState.letter.set()

    await CurrentGameHandler.init(state)
    hangman = await CurrentGameHandler.get(state)

    await message.answer(messages.GAME_MANUAL, reply_markup=get_alphabet_keyboard(hangman.used))
    await message.answer(MessageFormer.get_game_state_message(hangman))


@dp.message_handler(lambda message: message.text == buttons.END_GAME, state=GuessingState.letter)
async def process_end_game(message: Message, state: FSMContext):
    await state.finish()
    return await message.answer(messages.END_GAME, reply_markup=get_start_game_keyboard())


@dp.message_handler(lambda message: message.text == buttons.HINT, state=GuessingState.letter)
async def process_take_hint(message: Message, state: FSMContext):
    hangman = await CurrentGameHandler.get(state)
    return await message.answer(MessageFormer.get_hint_message(hangman))


@dp.message_handler(lambda message: message.text == buttons.GUESS_WORD, state=GuessingState.letter)
async def process_guess_word_request(message: Message):
    await GuessingState.word.set()
    return await message.answer(messages.TRY_GUESS_WORD)


@dp.message_handler(state=GuessingState.word)
async def process_guess_word(message: Message, state: FSMContext):
    word = message.text.upper()
    game = await CurrentGameHandler.get(state)

    if word == game.word:
        await state.finish()
        await message.answer(messages.WIN, reply_markup=get_start_game_keyboard())
    else:
        await GuessingState.letter.set()
        await message.answer(messages.INCORRECT_WORD, reply_markup=get_alphabet_keyboard(game.used))


@dp.message_handler(lambda message: message.text.upper() not in set(Hangman.ALPHABET), state=GuessingState.letter)
async def process_invalid_guess(message: Message):
    await message.reply(messages.INVALID_LETTER)


@dp.message_handler(lambda message: message.text.upper() in set(Hangman.ALPHABET), state=GuessingState.letter)
async def process_guess(message: Message, state: FSMContext):
    letter = message.text.upper()
    hangman = await CurrentGameHandler.get(state)

    if letter in hangman.used:
        await message.answer(messages.ALREADY_USED_LETTER)
        return

    is_try_success = hangman.is_successful_guess(letter)
    await CurrentGameHandler.update(state, hangman)

    if hangman.is_game_finished():
        await state.finish()
        await message.answer(MessageFormer.get_game_ending_message(hangman), reply_markup=get_start_game_keyboard())
    else:
        await message.reply(MessageFormer.get_try_result_message(is_try_success))
        await message.answer(MessageFormer.get_game_state_message(hangman), reply_markup=get_alphabet_keyboard(hangman.used))
