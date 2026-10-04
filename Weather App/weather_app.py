"""
Basic Weather App (Beginner Tier)

A command-line program that shows the current weather for a city or ZIP code
using the OpenWeatherMap "Current Weather Data" API (free tier).

The API key is read from the environment variable OPENWEATHER_API_KEY.
It is never written in this file.
"""

import os
import sys

import requests

API_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY_VARIABLE = "OPENWEATHER_API_KEY"
TIMEOUT_SECONDS = 10   # give up if the server does not answer in time
EXIT_WORDS = ("q", "quit", "exit")


def get_api_key():
    """Read the API key from the environment; exit with help if it is missing."""
    api_key = os.getenv(API_KEY_VARIABLE)
    if not api_key or not api_key.strip():
        print(f"Error: the environment variable {API_KEY_VARIABLE} is not set.")
        print("Setup (Windows Command Prompt):")
        print(f'    setx {API_KEY_VARIABLE} "your_api_key_here"')
        print("Then close and reopen your terminal / VS Code and run the program again.")
        print("Get a free key at https://openweathermap.org/api")
        sys.exit(1)
    return api_key.strip()


def get_city_input():
    """Ask for a city or ZIP code. Returns the text, or None if the user quits."""
    while True:
        text = input("\nEnter a city or ZIP code (or 'q' to quit): ").strip()  # strip() removes extra spaces

        if text.lower() in EXIT_WORDS:
            return None
        if text == "":
            print("Error: input cannot be empty. Please enter a city name or ZIP code.")
            continue
        return text


def build_request_params(location, api_key):
    """Build the query parameters. A leading number is treated as a ZIP code."""
    params = {"appid": api_key, "units": "metric"}  # metric = Celsius, wind in m/s

    first_part = location.split(",")[0].strip()
    if first_part.isdigit():
        params["zip"] = location.replace(" ", "")   # e.g. "94040,US" (country defaults to US)
    else:
        params["q"] = location                      # e.g. "London" or "Paris,FR"
    return params


def is_valid_weather_data(data):
    """Check that the JSON has every field we need, so later code cannot crash."""
    try:
        float(data["main"]["temp"])
        float(data["main"]["humidity"])
        float(data["wind"]["speed"])
        return bool(data["name"]) and bool(data["weather"][0]["description"])
    except (KeyError, IndexError, TypeError, ValueError):
        return False


def fetch_weather(location, api_key):
    """
    Call the API. Returns (data, None) on success or (None, error_message) on failure.
    Raw technical errors are never shown to the user.
    """
    params = build_request_params(location, api_key)

    try:
        response = requests.get(API_URL, params=params, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()   # raises HTTPError for 4xx / 5xx status codes
        data = response.json()        # parse the JSON text into a dictionary
    except requests.exceptions.Timeout:
        return None, "Error: the request timed out. Please try again."
    except requests.exceptions.ConnectionError:
        return None, "Error: could not connect. Check your internet connection."
    except requests.exceptions.HTTPError as error:
        status = error.response.status_code if error.response is not None else None
        if status == 401:
            return None, f"Error: invalid or unauthorized API key. Check {API_KEY_VARIABLE}. (New keys can take a couple of hours to activate.)"
        if status == 404:
            return None, f"Error: '{location}' was not found. Check the spelling or try 'City,CountryCode' (e.g. Paris,FR)."
        if status == 429:
            return None, "Error: API rate limit exceeded. Please wait a minute and try again."
        return None, f"Error: the weather service returned an error (code {status}). Please try again later."
    except ValueError:
        # response.json() fails when the reply is not valid JSON
        return None, "Error: received an unreadable response from the weather service."
    except requests.exceptions.RequestException:
        return None, "Error: the request failed. Please try again."

    if not is_valid_weather_data(data):
        return None, "Error: the weather service sent incomplete data. Please try again."
    return data, None


def display_weather(data):
    """Print the weather details in a neat format."""
    city = data["name"]
    country = data.get("sys", {}).get("country", "")
    celsius = float(data["main"]["temp"])
    fahrenheit = (celsius * 9 / 5) + 32      # Fahrenheit = (Celsius * 9/5) + 32
    humidity = data["main"]["humidity"]
    description = data["weather"][0]["description"].title()
    wind_speed = data["wind"]["speed"]

    place = f"{city}, {country}" if country else city
    print("\n" + "=" * 36)
    print(f"  Weather in {place}")
    print("=" * 36)
    print(f"  Temperature : {celsius:.1f} °C / {fahrenheit:.1f} °F")
    print(f"  Humidity    : {humidity}%")
    print(f"  Condition   : {description}")
    print(f"  Wind speed  : {wind_speed} m/s")
    print("=" * 36)


def main():
    """Run the program loop."""
    api_key = get_api_key()

    print("=" * 36)
    print("      BASIC WEATHER APP")
    print("=" * 36)
    print("Type a city name (e.g. London) or a ZIP code with country code (e.g. 94040,US).")
    print("Type 'q' at any prompt to quit.")

    while True:
        location = get_city_input()
        if location is None:
            print("Goodbye!")
            break

        data, error_message = fetch_weather(location, api_key)
        if error_message:
            print(error_message)
        else:
            display_weather(data)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram stopped. Goodbye!")
