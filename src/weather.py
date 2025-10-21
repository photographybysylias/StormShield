#!/usr/bin/env python3
# ==============================================
# StormShield — weather.py
# Author: Sylias Shufelt
# Purpose: Check for severe thunderstorm or
#          tornado warnings by U.S. ZIP code
#          using NOAA's public weather API.
# ==============================================

import requests

def storm_warning_detected(zip_code: str) -> bool:
    """
    Checks NOAA API for active thunderstorm or tornado alerts
    affecting a given ZIP code area.

    Args:
        zip_code (str): U.S. ZIP code (e.g., "46580")

    Returns:
        bool: True if an alert is active, else False.
    """
    try:
        # NOAA’s alerts API uses region/state filters (first 2 ZIP digits are enough)
        url = f"https://api.weather.gov/alerts/active?area={zip_code[:2]}"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        # Loop through all alerts
        for alert in data.get("features", []):
            props = alert.get("properties", {})
            event = props.get("event", "").lower()
            if any(term in event for term in ["thunderstorm", "tornado"]):
                print(f"[Weather] Active alert detected: {props.get('event')}")
                return True

        print("[Weather] No thunderstorm/tornado alerts currently active.")
        return False

    except Exception as e:
        print(f"[Weather] Error checking alerts: {e}")
        return False
