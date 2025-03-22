import json
import requests
import xmltodict as td
import time
import asyncio
from tornado.websocket import WebSocketHandler

class CurrencyObserver:
    def __init__(self):
        self._observers = set()
        self.currencies_data = None
        self.request_interval = 10  # Интервал запроса данных в секундах

    def register(self, observer):
        self._observers.add(observer)

    def unregister(self, observer):
        self._observers.discard(observer)

    async def notify_observers(self):
        for observer in self._observers:
            await observer.update(self.currencies_data)

    async def fetch_currencies(self, currencies_ids_lst: list):
        while True:
            xml_data = requests.get('http://www.cbr.ru/scripts/XML_daily.asp').content
            result = []
            data_dict = td.parse(xml_data)

            for currency in data_dict['ValCurs']['Valute']:
                if currency['CharCode'] in currencies_ids_lst or currency["Name"] in currencies_ids_lst:
                    value_parts = currency['Value'].split(',')
                    currency['Value'] = {
                        'integer_part': int(value_parts[0]),
                        'fractional_part': int(value_parts[1])
                    }
                    if currency['Nominal'] != '1':
                        currency['Nominal'] = int(currency['Nominal'])
                    result.append(currency)

            self.currencies_data = result
            await self.notify_observers()
            await asyncio.sleep(self.request_interval)

class CurrencyWebSocketHandler(WebSocketHandler):
    def initialize(self, observer):
        self.observer = observer

    async def open(self):
        self.observer.register(self)
        await self.write_message(json.dumps({"client_id": id(self)}))

    def on_close(self):
        self.observer.unregister(self)

    async def update(self, data):
        await self.write_message(json.dumps(data))