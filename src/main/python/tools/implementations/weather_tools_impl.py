"""
Standalone implementation of weather tools functions.
"""
import random

from app import App
from ..interfaces.weather_tools import Weather


def get_user_location() -> tuple[str, str]:
    """
    Returns a mock user location.
    
    Returns:
        tuple[str, str]: (county, state)
    """
    # Mock location - in real implementation this would get actual user location
    return ("King County", "Washington")


def get_geo_from_county(county: str, state: str) -> tuple[float, float]:
    """
    Returns mock coordinates based on some common locations.
    
    Args:
        county: County name
        state: State name
        
    Returns:
        tuple[float, float]: (latitude, longitude)
    """
    # Mock coordinates for some common locations
    location_coords = {
        ("King County", "Washington"): (47.6062, -122.3321),  # Seattle area
        ("Los Angeles County", "California"): (34.0522, -118.2437),  # Los Angeles
        ("Cook County", "Illinois"): (41.8781, -87.6298),  # Chicago
        ("Harris County", "Texas"): (29.7604, -95.3698),  # Houston
        ("Maricopa County", "Arizona"): (33.4484, -112.0740),  # Phoenix
    }
    
    # Return known coordinates or generate mock ones
    location_key = (county, state)
    if location_key in location_coords:
        return location_coords[location_key]
    else:
        # Generate mock coordinates (US-ish range)
        latitude = random.uniform(25.0, 49.0)  # Roughly continental US latitude range
        longitude = random.uniform(-125.0, -66.0)  # Roughly continental US longitude range
        return (latitude, longitude)


def get_local_weather(latitude: float, longitude: float) -> Weather:
    """
    Returns mock weather data.
    
    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        
    Returns:
        Weather: Mock weather object
    """
    # Generate mock weather data
    temperature_celsius = random.uniform(-10.0, 40.0)  # Temperature in Celsius
    temperature_fahrenheit = (temperature_celsius * 9/5) + 32  # Convert to Fahrenheit
    precipitation_chance_percent = random.uniform(0.0, 100.0)  # Precipitation chance 0-100%
    
    return Weather(temperature_fahrenheit, precipitation_chance_percent)


def call_llm(prompt: str) -> str:
    app = App()
    print(f"Calling LLM with prompt: {prompt}")
    return app.answer_with_prompt(prompt)

