import asyncio
import logging
import sys
import json

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F
from aiogram.utils.formatting import (
   Bold, as_list, as_marked_section
)
from recipes_handler import router
from token_data import TOKEN_tl

dp = Dispatcher()
dp.include_router(router)

@dp.message(Command('start'))
async def command_start_handler(message: Message) -> None:
   kb = [
      [
         types.KeyboardButton(text="Команды"),
         types.KeyboardButton(text="Описание бота"),
      ],
   ]
   keyboard = types.ReplyKeyboardMarkup(
      keyboard=kb,
      resize_keyboard=True,
   )
   await message.answer(f"Привет! С чего начнем?", reply_markup=keyboard)

@dp.message(F.text.lower() == "команды")
async def commands(message: types.Message):
   response = as_list(
      as_marked_section(
         Bold("Команды:"),
         "/category",
         "/meals",
         "/id",
         marker="®",
      ),
   )
   await message.answer(**response.as_kwargs())

@dp.message(F.text.lower() == "описание бота")
async def commands(message: types.Message):
   await message.answer('Я бот который предлагает рецепты блюд!!!')

@dp.message(Command('cancel'))
async def commands(message: types.Message):
   await state.clear()

async def main() -> None:
   bot = Bot(TOKEN_tl)
   await dp.start_polling(bot)

if __name__ == "__main__":
   logging.basicConfig(level=logging.INFO, stream=sys.stdout)
   asyncio.run(main())