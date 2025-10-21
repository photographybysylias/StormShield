#!/usr/bin/env python3
# ==============================================
# StormShield — config_loader.py
# Author: Sylias Shufelt
# Purpose: Load and validate user configuration
#          for StormShield from stormshield.conf.
# ==============================================

import configparser
import os

DEFAULT_CONF_PATH = "/etc/stormshield.conf"

def load_config(conf_path: str = DEFAULT_CONF_PATH) -> dict:
    """
    Loads the StormShield configuration file and returns a structured dict.

    Args:
        conf_path (str): Path to the configuration file.

    Returns:
        dict: Parsed configuration with sensible defaults.
    """
    config = configparser.ConfigParser()

    if not os.path.exists(conf_path):
        print(f"[ConfigLoader] Warning: Config file not found at {conf_path}. Using defaults.")
        return default_config()

    try:
        config.read(conf_path)

        conf = {
            "weather": {
                "zip_code": config.get("weather", "zip_code", fallback="46580"),
                "api_key": config.get("weather", "api_key", fallback=""),
                "check_interval": config.getint("weather", "check_interval", fallback=600),
            },
            "notifications": {
                "webhook_url": config.get("notifications", "webhook_url", fallback=""),
                "pre_shutdown_delay": config.getint("notifications", "pre_shutdown_delay", fallback=180),
            },
            "shutdown": {
                "ignore_users": [u.strip() for u in config.get("shutdown", "ignore_users", fallback="").split(",") if u.strip()],
                "skip_services": [s.strip() for s in config.get("shutdown", "skip_services", fallback="").split(",") if s.strip()],
                "linkstation_ip": config.get("shutdown", "linkstation_ip", fallback=""),
                "linkstation_user": config.get("shutdown", "linkstation_user", fallback="admin"),
                "linkstation_pass": config.get("shutdown", "linkstation_pass", fallback="password"),
            }
        }

        print(f"[ConfigLoader] Loaded configuration from {conf_path}")
        return conf

    except Exception as e:
        print(f"[ConfigLoader] Failed to load configuration: {e}")
        return default_config()


def default_config() -> dict:
    """
    Returns a minimal default configuration for StormShield.
    """
    return {
        "weather": {
            "zip_code": "46580",
            "api_key": "",
            "check_interval": 600,
        },
        "notifications": {
            "webhook_url": "",
            "pre_shutdown_delay": 180,
        },
        "shutdown": {
            "ignore_users": [],
            "skip_services": [],
            "linkstation_ip": "",
            "linkstation_user": "admin",
            "linkstation_pass": "password",
        }
    }
