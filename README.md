# StormShield
**Protect your home servers from power loss and data corruption.**
---
## Overview
#### **StormShield** is an open-source automation tool that detects incoming thunderstorms by ZIP code and safely shuts down your Linux-based servers before power surges or outages cause damage or data loss.
#### Designed for **home labs, hobby servers, and small setups**, it helps prevent data corruption and unexpected crashes - while still giving you control.

## Key Features
**Real-time weather monitoring**
- Pulls severe thunderstorm alerts by **U.S. Zip vode** from NOAA's free weather API.

**Smart auto-shutdown**
- Gracefully shuts down your configured devices (Linux servers, NAS units, etc.) before storms hit.
- Supports **SSH shutdown** and **HTTP/REST-based power-off endpoints** (for devices like Buffalo LinkStations).

**Webhook notifications**
- Sends an alert to your webhook URL (e.g.), Discord, Slack, Gotify, Pushover, etc.)
- Gives you a configurable grace period (default: 3 minutes) to cancel shutdowns.

**User-aware safety**
- If someone other than root is logged in, StormShield will **pause the shutdown** and **notify** instead - so no one loses work mid-session.

**Configurable exclusions**
- Skip certain devices or services (e.g., routers, firewalls, UPS) from shutdown.
- Ignore specific usernames that are safe to remain active.

**Free and open source**
- Build with Python and YAML - no proprietary APIs, no paid dependencies.
---
