#!/usr/bin/env python3
# ==============================================
# StormShield — shutdown_manager.py
# Author: Sylias Shufelt
# Purpose: Safely handle shutdown operations while
#          respecting active sessions and exclusions.
# ==============================================

import os
import subprocess
import psutil
from time import sleep

def get_logged_in_users() -> list:
    """
    Returns a list of currently logged-in usernames.
    """
    try:
        users = [u.name for u in psutil.users()]
        return list(set(users))
    except Exception as e:
        print(f"[ShutdownManager] Failed to get users: {e}")
        return []


def active_root_only(ignore_users: list) -> bool:
    """
    Determines if only root (or no one) is logged in, ignoring specified users.

    Args:
        ignore_users (list): Users to ignore (configured in stormshield.conf).

    Returns:
        bool: True if only root or no one else is logged in; False otherwise.
    """
    users = get_logged_in_users()
    filtered = [u for u in users if u not in ignore_users]
    return (len(filtered) == 0) or (filtered == ["root"])


def shutdown_linkstation(ip: str, username: str, password: str) -> bool:
    """
    Attempts to shut down a Buffalo LinkStation via its web API.

    Args:
        ip (str): Local IP of the LinkStation.
        username (str): Login username.
        password (str): Login password.

    Returns:
        bool: True if shutdown command succeeded, False otherwise.
    """
    import requests
    try:
        url = f"http://{ip}/shutdown"
        resp = requests.post(url, auth=(username, password), timeout=5)
        if resp.status_code in [200, 202, 204]:
            print(f"[ShutdownManager] LinkStation at {ip} shutting down...")
            return True
        else:
            print(f"[ShutdownManager] LinkStation shutdown failed (code {resp.status_code})")
            return False
    except Exception as e:
        print(f"[ShutdownManager] LinkStation shutdown error: {e}")
        return False


def shutdown_system(skip_services: list):
    """
    Safely shuts down the system unless excluded services are running.

    Args:
        skip_services (list): Service names to avoid shutting down with.
    """
    try:
        for svc in skip_services:
            for proc in psutil.process_iter(attrs=['name']):
                if svc.lower() in proc.info['name'].lower():
                    print(f"[ShutdownManager] Skipping shutdown — {svc} is still running.")
                    return False

        print("[ShutdownManager] Proceeding with system shutdown in 10 seconds...")
        sleep(10)
        subprocess.run(["sudo", "shutdown", "-h", "now"], check=False)
        return True

    except Exception as e:
        print(f"[ShutdownManager] Shutdown error: {e}")
        return False
