"""Sensors for Microsoft Teams presence."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.config_entries import ConfigEntry

from . import TeamsPresenceCoordinator
from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Teams presence sensors."""
    coordinator: TeamsPresenceCoordinator = entry.runtime_data
    async_add_entities([TeamsPresenceSensor(coordinator)])


class TeamsPresenceSensor(CoordinatorEntity[TeamsPresenceCoordinator], SensorEntity):
    """Expose the normalized status of the signed-in Teams account."""

    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(self, coordinator: TeamsPresenceCoordinator) -> None:
        """Initialize a presence sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_{coordinator.config_entry.entry_id}_status"
        self._attr_name = "Status Teams"
        self._attr_icon = "mdi:microsoft-teams"

    @property
    def native_value(self) -> str | None:
        """Return online, away, busy, on_meeting, offline, or unknown."""
        availability = self.coordinator.data.get("availability")
        activity = self.coordinator.data.get("activity")

        if activity == "InAMeeting":
            return "on_meeting"
        if availability == "Available":
            return "online"
        if availability in {"Away", "BeRightBack"}:
            return "away"
        if availability in {"Busy", "DoNotDisturb"}:
            return "busy"
        if availability == "Offline":
            return "offline"
        return "unknown"
