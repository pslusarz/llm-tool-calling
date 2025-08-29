"""
Weather tools interface definitions - standalone function signatures.
"""
from typing import Callable

# Function type aliases for the weather tools interface
GetUserLocationFunc = Callable[[], tuple[str, str]]
GetGeoFromCountyFunc = Callable[[str, str], tuple[float, float]]
GetLocalWeatherFunc = Callable[[float, float], 'Weather']
CallLLMFunc = Callable[[str], str]


"""INTERFACE DEFINITIONS"""

class Weather:
    """Weather data container"""
    def __init__(self, temperature_fahrenheit: float, precipitation_chance_percent: float):
        self.temperature_fahrenheit = temperature_fahrenheit
        self.precipitation_chance_percent = precipitation_chance_percent  # 0.0 to 100.0





def get_user_location() -> tuple[str, str]:
    """
    Returns:
    tuple[str, str]: (county, state)
    """
    ...


def get_geo_from_county(county: str, state: str) -> tuple[float, float]:
    """
    Returns:
    tuple[float, float]: (latitude, longitude)
    """
    ...


def get_local_weather(latitude: float, longitude: float) -> Weather:
    """
    Returns:
    Weather: Weather object with temperature and precipitation_chance attributes
    """
    ...


def call_llm(prompt: str) -> str:
    """Special function to call self with the additional context data returned by the functions. 
    Ensure returned data is integrated into the prompt, along with user's original question."""
    ...
