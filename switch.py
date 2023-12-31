"""Platform for switch integration."""
from __future__ import annotations

import logging

from .mustafa import MustafaInstance
import voluptuous as vol

from pprint import pformat

# Import the device class from the component that you want to support
import homeassistant.helpers.config_validation as cv
from homeassistant.components.switch import (PLATFORM_SCHEMA, SwitchEntity)
from homeassistant.const import CONF_NAME, CONF_IP_ADDRESS, CONF_PORT, CONF_UNIQUE_ID, STATE_ON
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

_LOGGER = logging.getLogger("mustafa")

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME): cv.string,
    vol.Required(CONF_IP_ADDRESS): cv.string,
    vol.Required(CONF_PORT): cv.string,
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
        "ip_address": config[CONF_IP_ADDRESS],
        "port": config[CONF_PORT],
        "unique_id": config[CONF_UNIQUE_ID]
    }
    
    add_entities([MustafaSwitch(switch)])

class MustafaSwitch(SwitchEntity):
    """Representation of an Mustafa switch."""

    def __init__(self, switch) -> None:
        """Initialize an MustafaSwitch."""
        _LOGGER.info(pformat(switch))
        self._switch = MustafaInstance(switch["ip_address"],switch["port"],switch["unique_id"])
        self._name = switch["name"]
        self._state = False

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
        self._state = await self._switch.turn_on()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Instruct the switch to turn off."""
        self._state = await self._switch.turn_off()
    
    async def async_toggle(self, **kwargs):
        """Instruct the switch to toggle."""
        self._state = await self._switch.toggle()

    def update(self) -> None:
        """Fetch new state data for this switch.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self._switch.is_on