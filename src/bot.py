import asyncio

from config import bot
from telegram.handlers import dp


async def stop():
    dp.stop_polling()
    await dp.wait_closed()
    await bot.close()


async def start():
    loop.create_task(dp.start_polling())
    await stop()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())
    loop.close()
