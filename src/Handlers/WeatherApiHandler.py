from typing import Any, List, Dict
from urllib import request, parse
from datetime import datetime
import json


class WeatherApiHandler:
    def __init__(self):
        self.url: str = "http://dataservice.accuweather.com/forecasts/v1/daily/5day/31868?metric=true&apikey=QtHvzccUucsZyLMxEEgDljX7McW8U1io"

    def get_weather_by_date(self, day: int, month: int, year: int) -> Dict:
        headers: Dict = {'Accept': 'application/json'}
        req: Any = request.Request(self.url, headers=headers, method='GET')
        try:
            resp: Any = request.urlopen(req)
            jsonResponse: Dict = json.loads(resp.read())
            weather: Dict = {}
            for forecast in jsonResponse["DailyForecasts"]:
                date: str = forecast["Date"].split('T')[0]
                splitedDate: List[str] = date.split('-')
                forecastYear: int = int(splitedDate[0])
                forecastMonth: int = int(splitedDate[1])
                forecastDay: int = int(splitedDate[2])
                if ((day == forecastDay) and (month == forecastMonth)
                        and (year == forecastYear)):
                    weather["minimum"]: float = round(
                        forecast["Temperature"]["Minimum"]["Value"])
                    weather["maximum"]: float = round(
                        forecast["Temperature"]["Maximum"]["Value"])
                    weather["dayMessage"]: str = forecast["Day"]["IconPhrase"]
                    weather["nightMessage"]: str = forecast["Night"][
                        "IconPhrase"]
                    break
            return weather
        except urllib.error.HTTPError as e:
            pass
