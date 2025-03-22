import json
import requests
import xmltodict as td
import time
import matplotlib.pyplot as plt

class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class CurrenciesLst(metaclass=SingletonMeta):
    def __init__(self, request_interval=1):
        self.request_interval = request_interval
        self.last_request_time = 0
        self.currencies_data = None

    def get_currencies(self, currencies_ids_lst: list) -> list:
        current_time = time.time()
        if current_time - self.last_request_time < self.request_interval:
            print("Запросы можно отправлять не чаще чем раз в", self.request_interval, "секунд.")
            return []

        self.last_request_time = current_time
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
        if result:
            for _v in result:
                print(f"Найдена валюта: {_v['Name']}, Курс: {_v['Value']['integer_part']}.{_v['Value']['fractional_part']}")
        else:
            print("Валюта не найдена.")
        return result

    def plot_currencies(self):
        if not self.currencies_data:
            print("Нет данных для построения графика.")
            return

        names = [currency['Name'] for currency in self.currencies_data]
        values = [currency['Value']['integer_part'] + currency['Value']['fractional_part'] / 100 for currency in self.currencies_data]

        plt.figure(figsize=(10, 5))
        plt.bar(names, values)
        plt.xlabel('Валюта')
        plt.ylabel('Курс (руб)')
        plt.title('Курсы валют ЦБ РФ')
        plt.savefig('currencies.jpg')
        plt.show()

# Тестируем
obj1 = CurrenciesLst(request_interval=1)
obj1.get_currencies(['GBP', 'KZT', 'Турецких лир'])
obj1.plot_currencies()

# Тесты
def test_incorrect_currency():
    obj = CurrenciesLst()
    result = obj.get_currencies(['R9999'])
    assert result == [], "Тест на неправильный код валюты не пройден"

def test_correct_currency():
    obj = CurrenciesLst()
    result = obj.get_currencies(['USD'])
    assert result and 0 < result[0]['Value']['integer_part'] < 999, "Тест на корректный код валюты не пройден"

test_incorrect_currency()
test_correct_currency()