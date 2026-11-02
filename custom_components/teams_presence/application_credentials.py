"""Microsoft OAuth application credentials support."""

from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_oauth2_flow

from homeassistant.components.application_credentials import ClientCredential

from .const import OAUTH2_AUTHORIZE, OAUTH2_SCOPES, OAUTH2_TOKEN


class MicrosoftOAuth2Implementation(
    config_entry_oauth2_flow.LocalOAuth2ImplementationWithPkce
):
    """OAuth implementation that requests only Teams presence read access."""

    @property
    def name(self) -> str:
        """Return the integration name for the account link flow."""
        return "Microsoft Teams Presence"

    @property
    def extra_authorize_data(self) -> dict[str, str]:
        """Return Microsoft Graph scopes and PKCE parameters."""
        return {
            **super().extra_authorize_data,
            "scope": OAUTH2_SCOPES,
            "response_mode": "query",
        }


async def async_get_auth_implementation(
    hass: HomeAssistant, auth_domain: str, credential: ClientCredential
) -> config_entry_oauth2_flow.AbstractOAuth2Implementation:
    """Return the OAuth implementation for the configured Azure app."""
    return MicrosoftOAuth2Implementation(
        hass,
        auth_domain,
        credential.client_id,
        OAUTH2_AUTHORIZE,
        OAUTH2_TOKEN,
        client_secret=credential.client_secret,
    )
