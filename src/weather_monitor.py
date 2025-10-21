#!/usr/bin/env python3
# ==============================================
# StormShield — weather_monitor.py
# Author: Sylias Shufelt
# Purpose: Fetch and interpret weather data
#          for storm detection by ZIP code.
# ==============================================

import requests
import time
import datetime

def fetch_weather(zip_code: str, api_key: str) -> dict:
    """
    Fetches weather data for a given ZIP code using Open-Meteo (free, no API key)
    or OpenWeatherMap if a key is provided.

    Args:
        zip_code (str): 5-digit U.S. ZIP code.
        api_key (str): Optional API key (for OpenWeatherMap).

    Returns:
        dict: Weather data (simplified structure).
    """
    try:
        if api_key:
            # Use OpenWeatherMap if a key is provided
            url = f"https://api.openweathermap.org/data/2.5/weather?zip={zip_code},US&appid={api_key}&units=imperial"
        else:
            # Use Open-Meteo for free weather data (no auth)
            url = f"https://api.open-meteo.com/v1/forecast?latitude=0&longitude=0&current=precipitation,weathercode"
            # For simplicity, latitude/longitude can be replaced via ZIP lookup
            # (ZIP-to-coord lookup handled elsewhere if desired)

        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json()

    except Exception as e:
        print(f"[WeatherMonitor] Failed to fetch weather: {e}")
        return {}


def detect_storm(weather_data: dict) -> bool:
    """
    Determines whether current conditions indicate a thunderstorm risk.

    Args:
        weather_data (dict): Data returned by fetch_weather().

    Returns:
        bool: True if thunderstorm detected, False otherwise.
    """
    try:
        # OpenWeatherMap code reference:
        # 2xx = Thunderstorm, 3xx = Drizzle, 5xx = Rain, 6xx = Snow, 7xx = Atmosphere, 800 = Clear
        if "weather" in weather_data:
            code = weather_data["weather"][0]["id"]
            if 200 <= code < 300:
                print(f"[WeatherMonitor] Thunderstorm detected (code {code}).")
                return True
        elif "current" in weather_data and "weathercode" in weather_data["current"]:
            code = weather_data["current"]["weathercode"]
            # 95-99 represent thunderstorm codes in Open-Meteo
            if code >= 95:
                print(f"[WeatherMonitor] Thunderstorm detected (code {code}).")
                return True

        return False

    except Exception as e:
        print(f"[WeatherMonitor] Error detecting storm: {e}")
        return False


def monitor(zip_code: str, api_key: str, interval: int = 600):
    """
    Periodically checks weather for storms.

    Args:
        zip_code (str): ZIP code to monitor.
        api_key (str): API key (optional).
        interval (int): Check frequency in seconds (default 10 min).
    """
    while True:
        data = fetch_weather(zip_code, api_key)
        if detect_storm(data):
            print(f"[WeatherMonitor] Storm conditions detected at {datetime.datetime.now()}")
            return True
        time.sleep(interval)
