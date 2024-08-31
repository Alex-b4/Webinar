import asyncio
import logging
import sys
import json
import aiohttp
import recipes_handler

from token_data import TOKEN_bd
from aiogram import Bot, Dispatcher, types, utils
from aiogram import F
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.context import FSMContext
from random import choices
from googletrans import Translator


translator = Translator()


async def choise_func(data):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                url=f'https://www.themealdb.com/api/json/v1/1/search.php?s={data['category']}',
                headers={'apikey': TOKEN_bd},
        ) as resp:
            meals = await resp.json()
    choise = choices(meals['meals'], k=data['number_recept'])
    receipt_name = []
    receipt_id = []
    for i in choise:
        # receipt_text = translator.translate(i['strInstructions'], dest='ru')
        receipt_id.append(i['idMeal'])
        receipt_name.append(translator.translate(i['strMeal'], dest='ru').text)
    id = ','.join(receipt_id)
    name = ', '.join(receipt_name)

    return id, name
