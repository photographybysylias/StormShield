#!/usr/bin/env python3
# ==============================================
# StormShield — main orchestration script
# Author: Sylias Shufelt
# Purpose: Monitor weather alerts by ZIP, safely
#          notify and shut down servers if needed.
# ==============================================

import yaml
from .weather import storm_warning_detected
from .notifier import notify_webhook
from .safety import wait_for_cancel, active_users_block_shutdown
from .shutdown_manager import perform_shutdown


def load_config():
    """
    Loads and parses the YAML configuration file.
    """
    try:
        with open("config/config.yaml", "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print("[StormShield] ERROR: config/config.yaml not found.")
        exit(1)
    except Exception as e:
        print(f"[StormShield] ERROR loading config: {e}")
        exit(1)


def main():
    """
    Main control logic for StormShield.
    1. Load configuration
    2. Check weather alerts
    3. Send notifications
    4. Handle cancel flags / user safety
    5. Shutdown if safe
    """
    cfg = load_config()
    zip_code = cfg["location"]["zip"]
    webhook = cfg["notification"]["webhook_url"]
    timeout = cfg["notification"]["cancel_timeout"]
    servers = cfg["shutdown"]["servers"]
    ignored_users = cfg["safety"]["ignore_users"]
    ignored_services = cfg["safety"]["ignore_services"]

    print(f"[StormShield] Monitoring ZIP {zip_code} for thunderstorm alerts...")

    if storm_warning_detected(zip_code):
        # 1️⃣ Alert user
        notify_webhook(
            webhook,
            "⛈️ Storm Alert",
            f"Thunderstorm detected near ZIP {zip_code}. "
            f"Shutdown in {timeout // 60} minutes unless canceled.",
            event="storm_detected"
        )

        # 2️⃣ Allow user to cancel shutdown
        if wait_for_cancel(timeout):
            print("[StormShield] Shutdown canceled. Returning to standby.")
            return

        # 3️⃣ Check for logged-in users
        active_users = active_users_block_shutdown(ignored_users)
        if active_users:
            msg = (
                f"Active user(s) detected: {', '.join(active_users)}. "
                "Manual shutdown recommended."
            )
            print(f"[StormShield] {msg}")
            notify_webhook(webhook, "⚠️ Active Users Detected", msg, event="manual_recommended")
            return

        # 4️⃣ No users — proceed with shutdown
        notify_webhook(
            webhook,
            "💤 Safe Shutdown",
            "No active users detected. Proceeding with system shutdown.",
            event="shutdown"
        )
        perform_shutdown(servers, ignored_services)

    else:
        print("[StormShield] No storm warnings detected. Standing by.")


if __name__ == "__main__":
    main()
