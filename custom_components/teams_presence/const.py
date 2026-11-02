"""Constants for the Microsoft Teams Presence integration."""

from datetime import timedelta

DOMAIN = "teams_presence"
PLATFORMS = ["sensor"]
SCAN_INTERVAL = timedelta(seconds=60)

OAUTH2_AUTHORIZE = (
    "https://login.microsoftonline.com/organizations/oauth2/v2.0/authorize"
)
OAUTH2_TOKEN = "https://login.microsoftonline.com/organizations/oauth2/v2.0/token"
OAUTH2_SCOPES = "offline_access https://graph.microsoft.com/Presence.Read"
GRAPH_PRESENCE_URL = "https://graph.microsoft.com/v1.0/me/presence"
