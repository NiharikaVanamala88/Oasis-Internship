# Basic Weather App

A beginner-level Python command-line application that retrieves current weather information for a city or ZIP code using the OpenWeatherMap API.

## Features

- Accepts a city name or ZIP code.
- Retrieves current weather data from OpenWeatherMap.
- Displays:
  - Temperature in °C and °F
  - Humidity
  - Weather condition
  - Wind speed
- Validates empty input.
- Handles API, network, timeout, authentication, and invalid-response errors.
- Allows multiple weather searches in one session.
- Reads the API key from the `OPENWEATHER_API_KEY` environment variable.
- Includes tests for API and error-handling scenarios.

## Technologies

- Python 3
- `requests`
- OpenWeatherMap API
- JSON

## Setup

Install the dependency:

```bash
pip install -r requirements.txt
```

Set your OpenWeatherMap API key as an environment variable.

**Windows PowerShell:**
```powershell
$env:OPENWEATHER_API_KEY="your_api_key"
```

**macOS/Linux:**
```bash
export OPENWEATHER_API_KEY="your_api_key"
```

Do not upload your API key to GitHub.

## Run

```bash
python weather_app.py
```

To run the tests:

```bash
python test_weather_app.py
```

## Project Structure

```text
Basic_Weather_App/
├── weather_app.py
├── requirements.txt
├── test_weather_app.py
└── README.md
```

## Concepts Used

API requests, JSON parsing, environment variables, input validation, exception handling, HTTP error handling, and automated testing.
