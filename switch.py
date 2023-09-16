"""Platform for switch integration."""
from __future__ import annotations

import logging

from .mustafa import MustafaInstance
import voluptuous as vol

from pprint import pformat

# Import the device class from the component that you want to support
import homeassistant.helpers.config_validation as cv
from homeassistant.components.switch import (PLATFORM_SCHEMA, SwitchEntity)
from homeassistant.const import CONF_NAME, CONF_IP_ADDRESS, CONF_MAC, CONF_UNIQUE_ID
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

_LOGGER = logging.getLogger("godox")

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME): cv.string,
    vol.Required(CONF_IP_ADDRESS): cv.string,
    vol.Required(CONF_MAC): cv.string,
    vol.Required(CONF_UNIQUE_ID): cv.string,
})


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the switch platform."""
    # Add devices
    _LOGGER.info(pformat(config))
    
    switch = {
        "name": config[CONF_NAME],
        "ip": config[CONF_IP_ADDRESS],
        "mac": config[CONF_MAC],
        "unique_id": config[CONF_UNIQUE_ID]
    }
    
    add_entities([MustafaSwitch(switch)])

class MustafaSwitch(SwitchEntity):
    """Representation of an Mustafa switch."""

    def __init__(self, switch) -> None:
        """Initialize an MustafaSwitch."""
        _LOGGER.info(pformat(switch))
        self._switch = MustafaInstance(switch["ip"],switch["mac"],switch["unique_id"])
        self._name = switch["name"]
        self._state = None

    @property
    def name(self) -> str:
        """Return the display name of this switch."""
        return self._name
    @property
    def unique_id(self):
        return self._switch._unique_id

    @property
    def is_on(self) -> bool | None:
        """Return true if switch is on."""
        return self._state

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Instruct the switch to turn on."""
        await self._switch.turn_on()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Instruct the switch to turn off."""
        await self._switch.turn_off()

    def update(self) -> None:
        """Fetch new state data for this switch.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self._switch.is_on