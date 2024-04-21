import json
import requests
from config import keys

class ConversationExeption(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def converts (base: str, quote: str, amount: str):
        if base == quote:
            raise ConversationExeption('Одинаковые валюты.')
        try:
            base_many = keys[base.lower()]
        except KeyError:
            raise ConversationExeption(f'Не удалось обработать валюту {base}')
        try:
            quote_many = keys[quote.lower()]
        except KeyError:
            raise ConversationExeption(f'Не удалось обработать валюту {quote}')
        try:
            amount = float(amount)
        except ValueError:
            raise ConversationExeption(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_many}'
                         f'&tsyms={quote_many.lower()}')
        total_out = json.loads(r.content)[quote_many]
        total_out = str(float(total_out) * float(amount))
        return total_out