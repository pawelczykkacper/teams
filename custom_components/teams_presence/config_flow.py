"""Config flow for Microsoft Teams Presence."""

import logging

from homeassistant.helpers import config_entry_oauth2_flow

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class OAuth2FlowHandler(
    config_entry_oauth2_flow.AbstractOAuth2FlowHandler, domain=DOMAIN
):
    """Handle Microsoft OAuth account linking."""

    DOMAIN = DOMAIN

    @property
    def logger(self) -> logging.Logger:
        """Return the flow logger."""
        return _LOGGER
