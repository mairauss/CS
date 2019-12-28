from typing import Any, List, Dict
import datetime
import unittest
from WeatherApiHandler import WeatherApiHandler


class TestingWeatherApiMethods(unittest.TestCase):
    def test_getWeatherByDate(self):
        dateWithTime: str = datetime.datetime.now()
        print(dateWithTime)
        day: int = dateWithTime.day
        month: int = dateWithTime.month
        year: int = dateWithTime.year
        api: WeatherApiHandler = WeatherApiHandler()
        weather: Dict = api.getWeatherByDate(day, month, year)

        # Must return the dict in form {'minimum': -2, 'maximum': 3, 'dayMessage': 'Mostly cloudy', 'nightMessage': 'Cloudy'}
        print(weather)

        weather: Dict = api.getWeatherByDate(25, 2, 3020)  # must be empty {}
        print(weather)
        self.assertEqual({}, weather)


if __name__ == '__main__':
    unittest.main()