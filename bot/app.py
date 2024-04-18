import telebot
from config import keys, TOKEN
from extension import CryptoConverter, ConversationExeption

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работы введите: \n<имя валюты, цену которой хотите узнать> ' \
           '<имя валюты, в которой надо узнать цену первой валюты>' \
           ' <количество первой валюты> \nПосмотреть все доступные валюты:  /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for a in keys.keys():
        text = '\n'.join((text, '- '+a))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConversationExeption('Слишком много параметров.')
        base, quote, amount = values
        total_out = CryptoConverter.converts(base, quote, amount)
    except ConversationExeption as e:
        bot.reply_to(message, f'Ошибка пользователя. \n {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду. \n {e}')
    else:
        if quote == 'рубль':
            text = f'Цена {amount} {base} в рублях составляет - {total_out}'
        else:
            text = f'Цена {amount} {base} в {quote}ах составляет - {total_out}'
        bot.send_message(message.chat.id, text)

bot.polling()