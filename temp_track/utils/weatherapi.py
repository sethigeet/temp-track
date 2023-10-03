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


def get_loc_name_from_loc(loc: str) -> str:
    """
    Gets the exact name of the location as retrieved in the weather data.

    args:
        loc: the name of the city or the ip address of a place.

    returns:
        a string containing the exact name of the location.
    """

    # Fetch the weather data
    res = requests.get(
        URL, params={"key": os.environ["WEATHERAPI_API_KEY"], "q": loc, "aqi": "no"}
    )
    data = res.json()

    match res.status_code:
        # Everything is all right!
        case HTTPStatus.OK:
            loc = data["location"]
            if loc["region"] == "":
                return f"{loc['name']}, {loc['country']}"
            return f"{loc['name']}, {loc['region']}, {loc['country']}"
        # API key is not valid
        case HTTPStatus.FORBIDDEN:
            raise InvalidAPIKeyException()
        # Data for given location is not available
        case HTTPStatus.BAD_REQUEST:
            raise DataUnavailableException()
        case _:
            raise WeatherAPIException(data["message"])


def get_curr_temp(loc: str) -> float | None:
    """
    Get the current temperature of the given location.

    args:
        loc: the name of the city or the ip address of a place.

    returns:
        the temperature of the location in degree celsius or None if there is no data for the location
    """

    # Fetch the weather data
    res = requests.get(
        URL, params={"key": os.environ["WEATHERAPI_API_KEY"], "q": loc, "aqi": "no"}
    )
    data = res.json()

    match res.status_code:
        # Everything is all right!
        case HTTPStatus.OK:
            return float(data["current"]["temp_c"])
        # API key is not valid
        case HTTPStatus.FORBIDDEN:
            raise InvalidAPIKeyException()
        # Data for given location is not available
        case HTTPStatus.BAD_REQUEST:
            raise DataUnavailableException()
        case _:
            raise WeatherAPIException(data["message"])


def api_key_is_valid() -> bool:
    """Checks whether the API key is valid or not."""

    # Make sure the api key is set in the environment variable
    api_key = os.environ["WEATHERAPI_API_KEY"]
    if api_key == "":
        return False

    try:
        # We know that data for loc: `mumbai` exists
        get_curr_temp("mumbai")
    except InvalidAPIKeyException:
        return False

    return True
