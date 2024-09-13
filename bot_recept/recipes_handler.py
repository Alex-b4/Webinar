import aiohttp
import json

from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.utils.formatting import (Bold, as_list, as_marked_section)
from utils import choise_func, zapros
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, types
from aiogram import F
from token_data import TOKEN_tl, TOKEN_bd
from googletrans import Translator
from keyboards import keyboard_start, keyboard_cat, keyboard_rec

translator = Translator()
router = Router()

class Receipt(StatesGroup):
    selection_unit = State()
    selection_number = State()
    choise_receipt = State()
    show_receipt = State()

@router.message(F.text.lower() == "команды")
async def commands(message: types.Message):
   response = as_list(
      as_marked_section(
         Bold("Команды:"),
         "/category - представляет список всех возможных категорий",
         "/meals - показывает случайный рецепт",
         marker="®",
      ),
   )
   await message.answer(**response.as_kwargs())

@router.message(F.text.lower() == "описание бота")
async def commands(message: types.Message):
   await message.answer('Я бот который предлагает рецепты блюд!!!')

@router.message(Command('cancel'))
async def commands(message: types.Message):
   await state.clear()

@router.message(Command('start'))
async def command_start_handler(message: Message) -> None:
   await message.answer(f"Привет! С чего начнем?", reply_markup=keyboard_start())
   await state.clear()

@router.message(Command('category')) # обработка команды категория
async def category(message: Message, state: FSMContext):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                url='https://www.themealdb.com/api/json/v1/1/list.php?c=list', headers={'apikey': TOKEN_bd},
        ) as resp:
            data_res = await resp.json()

        # вывод на экран всех возможных категорий
        await message.answer(f"Выбери категорию:", reply_markup= keyboard_cat(data_res) )
        await state.set_state(Receipt.selection_unit.state)

@router.message(Receipt.selection_unit) # обработываем выбранную категорию и узнаем сколько рецептов в ней
async def category_procesing(message: Message, state: FSMContext, number_recept=0):
    await state.update_data({'category': message.text.lower()})
    async with aiohttp.ClientSession() as session:
        async with session.get(
                url=f'https://www.themealdb.com/api/json/v1/1/filter.php?c={message.text.lower()}', headers={'apikey': TOKEN_bd},
        ) as res:
            data = await res.json()
    for i in data['meals']:
        number_recept += 1
    await message.answer('Какое количество блюд показать?')
    await state.update_data({'category_limit': number_recept})
    await state.set_state(Receipt.selection_number.state)

@router.message(Receipt.selection_number) # запрос на количество рецептов и проверка такого количества в категории
async def choose_number_reception(message: Message, state: FSMContext):
    data = await state.get_data()

    # проверка корректности ввода количества блюд
    if message.text.lower().isdigit():
        pass
    else:
        await message.answer('Некорректный формат ввоода!!!')
        return
    if int(message.text.lower()) > data['category_limit']:
        await message.answer('Количество блюд больше чем есть в базе. Уменьшите амбиции!!!')
        return
    await state.update_data({'number_recept': int(message.text.lower())})
    data = await state.get_data()
    id, name = await choise_func(data)
    await message.answer(f'Как Вам такие рецепты: {name}')
    await message.answer(f'Показать рецепты?', reply_markup=keyboard_rec())
    await state.update_data({'id': id})
    await state.set_state(Receipt.show_receipt.state)

@router.message(F.text.lower() == "покажи рецепты", Receipt.show_receipt)
async def recepr_show(message: Message, state: FSMContext):
    data = await state.get_data()
    data_id = str(data['id'])
    data_id = data_id.split(',')
    for i in data_id:
        recept, ingrid = await zapros(int(i)) # приложение обрабатывает рецепт и выдает результат
        response = as_list(
            Bold(translator.translate(recept['meals'][0]['strMeal'], dest='ru').text),
            Bold('Рецепт:'),
            translator.translate(recept['meals'][0]['strInstructions'], dest='ru').text,
            Bold('Ингридиенты:'), ingrid,
        )
        await message.answer(**response.as_kwargs())

@router.message(F.text.lower() == "предложи другие!!!", Receipt.show_receipt)
async def recepr_show(message: Message, state: FSMContext):
    await state.update_data({'id': None})
    data = await state.get_data()
    id, name = await choise_func(data)
    await message.answer(f'Как Вам такие рецепты: {name}')
    await message.answer(f'Показать рецепты?', reply_markup=keyboard_rec())
    await state.update_data({'id': id})