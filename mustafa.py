# define a platform for switch in home assistant
import asyncio
from homeassistant.const import STATE_ON, STATE_OFF
from .ip_switch import IpSwitch
import logging

LOGGER = logging.getLogger(__name__)
GATEWAY = "192.168.1.6"
GATEWAY_PORT = "8080"
async def discover():
    """Discover devices."""
    devices = await IpSwitch.discover_devices(GATEWAY,GATEWAY_PORT)
    LOGGER.debug("Discovered devices: %s", [{"address": device.ip, "name": device.name} for device in devices])
    return [device for device in devices if device.name.startswith("switch")]

            
class MustafaInstance:
    def __init__(self,ip_address,port :str,unique_id:str) -> None:
        self._ip_address = ip_address
        self._port = port
        self._device = IpSwitch(self._ip_address,self._port)
        self._state = None
        self._connected = None
        self._unique_id = unique_id
        
    async def _send(self, data: str):
        LOGGER.debug("sending: " + data)
        if (not self._connected):
            await self.connect()
        await self._device.send(data)
        pass
    
    @property
    def ip_address(self):
        return self._ip_address
    
    @property
    def port(self):
        return self._port
    
    @property
    def unique_id(self):
        return self._unique_id
    
    @property
    async def is_on(self):
        return await self._state
    
    async def turn_on(self):
        await self._device.send_data("on")
        self._state = STATE_ON
        
    async def turn_off(self):
        await self._device.send_data("off")
        self._state = STATE_OFF
        
    async def connect(self):
        # await self._device.connect()
        self._connected = True
        
    async def disconnect(self):
        await self._device.disconnect()
        self._connected = False