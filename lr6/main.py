import json
import requests
import xmltodict as td
import time
import matplotlib.pyplot as plt

class CurrenciesList:
    def __init__(self, request_interval=1):
        self.request_interval = request_interval
        self.last_request_time = 0
        self.currencies_data = None

    def get_currencies(self, currencies_ids_lst: list) -> list:
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

class CurrencyDecorator:
    def __init__(self, component):
        self._component = component

    def get_currencies(self, currencies_ids_lst: list):
        return self._component.get_currencies(currencies_ids_lst)

class ConcreteDecoratorJSON(CurrencyDecorator):
    def get_currencies(self, currencies_ids_lst: list):
        data = self._component.get_currencies(currencies_ids_lst)
        return json.dumps(data, ensure_ascii=False, indent=4)

class ConcreteDecoratorCSV(CurrencyDecorator):
    def get_currencies(self, currencies_ids_lst: list):
        data = self._component.get_currencies(currencies_ids_lst)
        if not data:
            return "Данные не найдены."

        csv_output = "Name,CharCode,Nominal,Value\n"
        for currency in data:
            value = f"{currency['Value']['integer_part']}.{currency['Value']['fractional_part']}"
            csv_output += f"{currency['Name']},{currency['CharCode']},{currency['Nominal']},{value}\n"

        return csv_output

# Тестируем
base_currencies = CurrenciesList(request_interval=1)
json_currencies = ConcreteDecoratorJSON(base_currencies)
csv_currencies = ConcreteDecoratorCSV(base_currencies)

# Получаем данные в формате JSON
json_data = json_currencies.get_currencies(['GBP', 'KZT', 'Турецкая лира'])
print("JSON Data:")
print(json_data)

# Получаем данные в формате CSV
csv_data = csv_currencies.get_currencies(['GBP', 'KZT', 'Турецкая лира'])
print("CSV Data:")
print(csv_data)
