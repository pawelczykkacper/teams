"""Microsoft Teams presence integration for Home Assistant."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import aiohttp_client
from homeassistant.helpers.config_entry_oauth2_flow import (
    OAuth2Session,
    async_get_config_entry_implementation,
)

from .const import DOMAIN, PLATFORMS
from .coordinator import TeamsPresenceCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Teams presence from a config entry."""
    implementation = await async_get_config_entry_implementation(hass, entry)
    oauth_session = OAuth2Session(hass, entry, implementation)
    session = aiohttp_client.async_get_clientsession(hass)
    coordinator = TeamsPresenceCoordinator(hass, entry, session, oauth_session)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
