"""Data coordinator and Microsoft Graph client."""

from __future__ import annotations

import logging
from typing import Any

from aiohttp import ClientError, ClientResponseError, ClientSession
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, HomeAssistantError
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.config_entry_oauth2_flow import OAuth2Session

from .const import DOMAIN, GRAPH_PRESENCE_URL, SCAN_INTERVAL


class TeamsPresenceCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Fetch signed-in user's Teams presence from Microsoft Graph."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        session: ClientSession,
        oauth: OAuth2Session,
    ) -> None:
        """Initialize coordinator."""
        super().__init__(
            hass,
            logging.getLogger(__name__),
            config_entry=entry,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )
        self._session = session
        self._oauth = oauth

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch presence data, refreshing OAuth tokens when needed."""
        await self._oauth.async_ensure_token_valid()
        try:
            async with self._session.get(
                GRAPH_PRESENCE_URL,
                headers={"Authorization": f"Bearer {self._oauth.token['access_token']}"},
            ) as response:
                if response.status == 401:
                    raise ConfigEntryAuthFailed("Microsoft Graph rejected the token")
                response.raise_for_status()
                return await response.json()
        except ConfigEntryAuthFailed:
            raise
        except ClientResponseError as err:
            raise UpdateFailed(f"Microsoft Graph returned HTTP {err.status}") from err
        except (ClientError, HomeAssistantError) as err:
            raise UpdateFailed(f"Unable to fetch Teams presence: {err}") from err
