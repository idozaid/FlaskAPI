from flask import Blueprint, request
import asyncio
from werkzeug.exceptions import HTTPException

from config import *


flask_routes = Blueprint('flask_routes', __name__)


@flask_routes.route("/weather/coldest/", methods=['GET'])
async def get_coldest():
    name_list = [city.name for city in cities_dict.values()]
    temp_list = await asyncio.gather(*[city.temp for city in cities_dict.values()])

    city_list = [{name: temp} for (name, temp) in zip(name_list, temp_list)]
    return min(city_list, key=lambda city: list(city.values())[0])


@flask_routes.route("/weather/warmest/", methods=['GET'])
async def get_warmest():
    name_list = [city.name for city in cities_dict.values()]
    temp_list = await asyncio.gather(*[city.temp for city in cities_dict.values()])

    city_list = [{name: temp} for (name, temp) in zip(name_list, temp_list)]
    return max(city_list, key=lambda city: list(city.values())[0])


@flask_routes.route("/weather/overrides/<city_name>/create/", methods=['POST'])
def override_temperature(city_name: str):
    # Get wanted temp
    try:
        temp = float(request.args.get('temp'))
    except:
        return failure('Wrong parameter inserted')

    if city_name and city_name in cities_dict.keys():
        # Check if already overridden
        if city_name in OverriddenCitiesFile():
            OverriddenCitiesFile.change_city_temp(city_name, temp)
        else:
            OverriddenCitiesFile.add_city(city_name, temp)
        return success()
    else:
        return failure('City not in list')


@flask_routes.route("/weather/overrides/list/", methods=['GET'])
def get_overridden_cities():
    return success(OverriddenCitiesFile.get_city_dict())


@flask_routes.route("/weather/overrides/<city_name>/", methods=['DELETE'])
def delete_override(city_name: str):
    if OverriddenCitiesFile.get_temp(city_name):
        OverriddenCitiesFile.delete_city(city_name)
        return success()
    else:
        return failure('City did not overridden')


@flask_routes.app_errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

