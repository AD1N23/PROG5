import requests
import json


city, lat, lon = "Saint Petersburg, RU", 59.57, 30.19
api_key = '4043542ad6be339bfb71d54d4a5e7991'
dt = 1671354770

req = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&dt={dt}&appid={api_key}')

req_obj = json.loads(req.text)  # Преобразуем объект типа Request в json-формат
# print(req_obj)

def getweather(api_key=None):
    import json
    import requests
    city, lat, lon = "Saint Petersburg, RU", 59.57, 30.19

    dt = 1671354770  # datetime of Wed Dec 18 2022 19:54:50 GMT+0000 in unix-like format
    # Для определения unixtime диапазона для получения температур,
    # можно использовать сервис https://unixtime-converter.com/

    if api_key:
        result = dict()
        req = requests.get(
            f'http://api.openweathermap.org/data/2.5/forecast?'
            f'lat={lat}&lon={lon}&dt={dt}&'
            f'appid={api_key}&lang=ru&units=metric')

        # для других параметров см. https://openweathermap.org/api/one-call-api#history

        req_obj = json.loads(req.text)  # Преобразуем объект типа Request в json-формат
        print(json.dumps(req_obj))
        # Сохраним результаты температур в формате json, чтобы ниже их визуализировать
        result['city'] = city
        measures = [{"dt": str(measure['dt']), "temp": str(measure['main']['temp'])} for measure in req_obj["list"]]


        result['temps'] = measures
        return json.dumps(result)


weather_data_json = getweather(api_key)

def visualise_data(json_data=''):
    if json_data:
        import matplotlib.pyplot as plt
        import pandas as pd
        from datetime import datetime, timezone

        data = pd.read_json(json_data)
        city_name = data['city']

        dates = [datetime.fromtimestamp(int(_d['dt']), tz=timezone.utc).strftime('%Y-%m-%d %H:%M') for _d in data['temps'][:]]
        temps = [float(_t['temp']) for _t in data['temps'][:]]

     
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))


        ax1.scatter(dates, temps, color='blue')
        ax1.set_title(f'Температура в городе {city_name}')
        ax1.set_xlabel('Дата и время')
        ax1.set_ylabel('Температура (°C)')
        ax1.set_xticks(dates[::2])  
        ax1.tick_params(axis='x', rotation=45)  

     
        ax2.boxplot(temps, vert=False)
        ax2.set_title('Распределение температур')
        ax2.set_xlabel('Температура (°C)')

       
        plt.subplots_adjust(left=0.1, right=0.9, bottom=0.2, top=0.9, hspace=0.5)  

 
        pos1 = ax1.get_position() 
        pos2 = ax2.get_position() 

   
        ax2.set_position([pos2.x0, pos2.y0 - 0.05, pos2.width, pos2.height * 0.8])

        plt.show()

visualise_data(weather_data_json)