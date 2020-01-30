from typing import Any, List, Dict
from urllib import request, parse, error
from datetime import datetime
import json


class WeatherApiHandler:
    def __init__(self):
        self.url: str = "http://api.openweathermap.org/data/2.5/forecast?id=2761369&APPID=72362c0ff6f6477793e4cea3416b1255&units=metric"

    def get_weather_by_date(self, day: int, month: int, year: int) -> Dict:
        headers: Dict = {'Accept': 'application/json'}
        req: Any = request.Request(self.url, headers=headers, method='GET')
        try:
            resp: Any = request.urlopen(req)
            jsonResponse: Dict = json.loads(resp.read())
            weather: Dict = {}
            temperatures:List[float] = []
            dayMessage: str = ''
            nightMessage: str = ''
            for forecast in jsonResponse["list"]:
                date: str = forecast["dt_txt"].split(' ')[0]
                time: str = forecast["dt_txt"].split(' ')[1]
                splitedDate: List[str] = date.split('-')
                forecastYear: int = int(splitedDate[0])
                forecastMonth: int = int(splitedDate[1])
                forecastDay: int = int(splitedDate[2])
                if ((day == forecastDay) and (month == forecastMonth)
                        and (year == forecastYear)):
                    temperature: float = forecast['main']['temp']
                    temperatures.append(temperature)
                    if((time == '22:00:00') or (time == '00:00:00') or (time == '03:00:00') or (time == '06:00:00')):
                        nightMessage = forecast['weather'][0]['description']
                    else:
                        dayMessage = forecast['weather'][0]['description']

            weather["minimum"]: float = round(min(temperatures))
            weather["maximum"]: float = round(max(temperatures))
            weather["dayMessage"]: str = nightMessage
            weather["nightMessage"]: str = dayMessage
            return weather
        except error.HTTPError as e:
            pass
