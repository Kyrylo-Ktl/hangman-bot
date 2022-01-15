from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from environs import Env

env = Env()
env.read_env('.env')

DICTIONARY_FILE = env('DICTIONARY_FILE')
MASK_SYMBOL = env('MASK_SYMBOL')
LIVE_SYMBOL = env('LIVE_SYMBOL')
MIN_WORD_LEN = env.int('MIN_WORD_LEN')
MAX_WORD_LEN = env.int('MAX_WORD_LEN')
LIVES_COUNT = env.int('LIVES_COUNT')

API_TOKEN = env('API_TOKEN')

# Create a bot
bot = Bot(token=API_TOKEN)

# Initializing temporary in-memory storage
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)
