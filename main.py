import aiogram
import asyncio
import database

from aiogram.utils import executor
from bot import dp as main_dp
from create_bot import dp, bot, logger

async def on_startup(self):
    await database.start_db()

    logger.info('Bot started')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

