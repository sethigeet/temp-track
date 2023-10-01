import os
from http import HTTPStatus
import requests

URL = "http://api.weatherapi.com/v1/current.json"


class WeatherAPIException(Exception):
    """A generic exception for any error that occurs in weatherapi."""


class InvalidAPIKeyException(Exception):
    """The API key is either not set in the environment variable or is not valid."""


class DataUnavailableException(Exception):
    """The weather data for the given location is not available."""


def get_temp(loc: str) -> int | None:
    """
    Get the temperate of the given location.

    args:
        loc: the name of the city or the ip address of a place.

    returns:
        the temperature of the location in degree celsius or None if there is no data for the location
    """

    # Make sure the api key is set in the environment variable
    api_key = os.environ["WEATHERAPI_API_KEY"]
    if api_key == "":
        raise InvalidAPIKeyException()

    # Fetch the weather data
    res = requests.get(URL, params={"key": api_key, "q": loc, "aqi": "no"})
    data = res.json()

    match res.status_code:
        # Everything is all right!
        case HTTPStatus.OK:
            return data["current"]["temp_c"]
        # API key is not valid
        case HTTPStatus.FORBIDDEN:
            raise InvalidAPIKeyException()
        # Data for given location is not available
        case HTTPStatus.BAD_REQUEST:
            raise DataUnavailableException()
        case _:
            raise WeatherAPIException(data["message"])


"""
{'error': {'code': 1006, 'message': 'No matching location found.'}}

{
  "location": {
    "name": "Mumbai",
    "region": "Maharashtra",
    "country": "India",
    "lat": 18.98,
    "lon": 72.83,
    "tz_id": "Asia/Kolkata",
    "localtime_epoch": 1696167655,
    "localtime": "2023-10-01 19:10"
  },
  "current": {
    "last_updated_epoch": 1696167000,
    "last_updated": "2023-10-01 19:00",
    "temp_c": 30.0,
    "temp_f": 86.0,
    "is_day": 0,
    "condition": {
      "text": "Moderate or heavy rain shower",
      "icon": "//cdn.weatherapi.com/weather/64x64/night/356.png",
      "code": 1243
    },
    "wind_mph": 6.9,
    "wind_kph": 11.2,
    "wind_degree": 230,
    "wind_dir": "SW",
    "pressure_mb": 1005.0,
    "pressure_in": 29.68,
    "precip_mm": 0.02,
    "precip_in": 0.0,
    "humidity": 89,
    "cloud": 100,
    "feelslike_c": 37.0,
    "feelslike_f": 98.6,
    "vis_km": 2.5,
    "vis_miles": 1.0,
    "uv": 1.0,
    "gust_mph": 17.0,
    "gust_kph": 27.4
  }
}
"""
