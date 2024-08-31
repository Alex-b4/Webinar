import aiohttp
import json
from datetime import datetime

from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.formatting import (Bold, as_list, as_marked_section)
from utils import choise_func
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, types
from aiogram import F
from token_data import TOKEN_tl
from token_data import TOKEN_bd
from googletrans import Translator


translator = Translator()
router = Router()

class Receipt(StatesGroup):
    selection_unit = State()
    selection_number = State()
    choise_receipt = State()
    show_receipt = State()

@router.message(Command('category')) # обработка команды категория
async def category(message: Message, state: FSMContext):
    # if command.args is None:
    #     await message.answer("Ошибка: не переданы аргументы")
    #     return
    # await state.set_data({'aver': int(command.args)})
    async with aiohttp.ClientSession() as session:
        async with session.get(
                url='https://www.themealdb.com/api/json/v1/1/list.php?c=list', headers={'apikey': TOKEN_bd},
        ) as resp:
            data_res = await resp.json()
        # вывод на экран всех возможных категорий
        builder = ReplyKeyboardBuilder()
        for i in data_res['meals']:
            # name_cat = translator.translate(i['strCategory'], dest='ru')
            builder.add(types.KeyboardButton(text= i['strCategory']))
        builder.adjust(4)
        await message.answer(f"Выбери категорию:",
            reply_markup=builder.as_markup(resize_keyboard=True),
        )
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
    if int(message.text.lower()) > data['category_limit']:
        await message.answer('Количество блюд больше чем есть в базе. Уменьшите амбиции!!!')
        return
    await state.update_data({'number_recept': int(message.text.lower())})
    data = await state.get_data()
    while message.text != 'Показать рецепты?':
        id, name = await choise_func(data)
        await message.answer(f'Как Вам такие рецепты: {name}')
        kb = [
            [
                types.KeyboardButton(text="Покажи рецепты"),
                types.KeyboardButton(text='Предложи другие!!!'),
            ],
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
        )
        mes = await message.answer(f'Показать рецепты?', reply_markup=keyboard)
        await router.register_next_step_handler(mes, choose_number_reception)
    await state.update_data({'id': id})
    await state.set_state(Receipt.show_receipt.state)

@router.message(F.text.lower() == "покажи рецепты", Receipt.show_receipt)
async def recepr_show(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(str(data['id']))

@router.message(F.text.lower() == "предложи другие!!!", Receipt.show_receipt)
async def recepr_show(message: Message, state: FSMContext):
    await state.update_data({'id': None})
    await state.set_state(Receipt.selection_number.state)