import asyncio
import sys
import json
import aiohttp

from token_data import TOKEN_bd
from aiogram import Bot, Dispatcher, types, utils
from aiogram import F
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
        receipt_id.append(i['idMeal'])
        receipt_name.append(translator.translate(i['strMeal'], dest='ru').text)
    id = ','.join(receipt_id)
    name = ', '.join(receipt_name)

    return id, name

async def zapros(i):
    sch_ = 1
    ingrid = ''
    async with aiohttp.ClientSession() as session:
        async with session.get(
                url=f'https://www.themealdb.com/api/json/v1/1/lookup.php?i={i}',
                headers={'apikey': TOKEN_bd},
        ) as resp:
            meals = await resp.json()
        while meals['meals'][0][f'strIngredient{sch_}'] != '':
            ingrid += (f'{translator.translate(meals['meals'][0][f'strIngredient{sch_}'], dest='ru').text}: '
                       f'{translator.translate(meals['meals'][0][f'strMeasure{sch_}'], dest='ru').text}; \n')
            sch_ += 1
            if f'strIngredient{sch_}' in meals['meals'][0]:
                pass
            else:
                break
    return meals, ingrid