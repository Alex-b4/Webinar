import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types
from recipes_handler import router
from token_data import TOKEN_tl

dp = Dispatcher()
dp.include_router(router)

async def main() -> None:
   bot = Bot(TOKEN_tl)
   await dp.start_polling(bot)

if __name__ == "__main__":
   logging.basicConfig(level=logging.INFO, stream=sys.stdout)
   asyncio.run(main ())