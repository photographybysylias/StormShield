#!/usr/bin/env python3
# ==============================================
# StormShield — notifier.py
# Author: Sylias Shufelt
# Purpose: Send alerts and status updates to
#          a configured webhook URL.
# ==============================================

import requests
import json
import datetime

def send_notification(webhook_url: str, title: str, message: str) -> bool:
    """
    Sends a formatted message to a webhook URL (e.g., Discord).

    Args:
        webhook_url (str): Full URL of the webhook endpoint.
        title (str): Short title for the message.
        message (str): Body text to include in the message.

    Returns:
        bool: True if the request succeeded, False otherwise.
    """
    try:
        timestamp = datetime.datetime.utcnow().isoformat()

        payload = {
            "embeds": [
                {
                    "title": f"⚠️ {title}",
                    "description": message,
                    "color": 16711680,  # Red
                    "footer": {"text": f"StormShield • {timestamp} UTC"}
                }
            ]
        }

        headers = {"Content-Type": "application/json"}
        resp = requests.post(webhook_url, data=json.dumps(payload), headers=headers, timeout=10)
        resp.raise_for_status()

        print(f"[Notifier] Sent notification: {title}")
        return True

    except Exception as e:
        print(f"[Notifier] Failed to send notification: {e}")
        return False
