from dataclasses import dataclass
import os
import aiohttp
import json


API_KEY = os.getenv('WEATHER_API_KEY')
CITY_LIST_FILE_PATH = 'C:\\Users\\Administrator\\Desktop\\Ido\\Training\\FlaskAPI\\FlaskAPI\\city_list.txt'

WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather'


def success(info=None):
    if info:
        return {'Success': True} | info
    else:
        return {'Success': True}

def failure(reason: str):
    return {'Success': False, 'Reason': reason}


@dataclass
class City:
    name: str

    @property
    async def temp(self, is_async=False):
        overridden_dict = OverriddenCitiesFile.get_city_dict()
        url_params = {'q': self.name, 'units': 'metric', 'appid': API_KEY}
        
        if self.name in overridden_dict:
            return overridden_dict.get(self.name)

        async with aiohttp.ClientSession() as session:
            async with session.get(WEATHER_API_URL, params=url_params) as result:
                return (await result.json())['main']['temp']


    @temp.setter
    def temp(self, temp):
        self.temp = temp


# Initialize cities dict from file
cities_dict = {city: City(city) for city in open(CITY_LIST_FILE_PATH).read().split('\n')}

class OverriddenCitiesFile():
    file_path = 'C:\\Users\\Administrator\\Desktop\\Ido\\Training\\FlaskAPI\\FlaskAPI\\overridden.json'

    def __contains__(self, item):
        if item in self.get_city_dict().keys():
            return True
        else:
            return False

    @classmethod
    def get_city_dict(cls):
        with open(cls.file_path, 'r') as overridden_file:
            overridden_dict = json.load(overridden_file)
        return overridden_dict

    @classmethod
    def write_to_file(cls, dict_to_write):
        with open(cls.file_path, 'w') as overridden_file:
            json.dump(dict_to_write, overridden_file)

    @classmethod
    def add_city(cls, city, temp):
        overridden_dict = cls.get_city_dict()

        cls.write_to_file(overridden_dict | {city: temp})

    @classmethod
    def change_city_temp(cls, city, temp):
        overridden_dict = cls.get_city_dict()
        overridden_dict[city] = temp

        cls.write_to_file(overridden_dict)

    @classmethod
    def delete_city(cls, city):
        overridden_dict = cls.get_city_dict()
        overridden_dict.pop(city)

        cls.write_to_file(overridden_dict)

    @classmethod
    def get_temp(cls, city):
        overridden_dict = cls.get_city_dict()
        if city not in overridden_dict.keys():
            return False
        else:
            return overridden_dict[city]