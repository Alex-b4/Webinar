from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def keyboard_start():
    kb = [
        [
            types.KeyboardButton(text="Команды"),
            types.KeyboardButton(text="Описание бота")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    return keyboard

def keyboard_cat(data):

    builder = ReplyKeyboardBuilder()
    for i in data['meals']:
        builder.add(types.KeyboardButton(text=i['strCategory']))
    builder.adjust(4)

    return builder.as_markup(resize_keyboard=True)

def keyboard_rec():
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
    return keyboard
