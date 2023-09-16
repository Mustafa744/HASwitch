# define a platform for switch in home assistant
import asyncio
from .ip_switch import IpSwitch
import logging

LOGGER = logging.getLogger(__name__)
GATEWAY = "localhost"
GATEWAY_PORT = "8080"
async def discover():
    """Discover devices."""
    devices = await IpSwitch.discover_devices(GATEWAY,GATEWAY_PORT)
    LOGGER.debug("Discovered devices: %s", [{"address": device.ip, "name": device.name} for device in devices])
    return [device for device in devices if device.name.startswith("switch")]

            
class MustafaInstance:
    def __init__(self,host:str,port:str,unique_id:str) -> None:
        self._host = host
        self._port = port
        self._device = IpSwitch(self.host,self.port)
        self._is_on = None
        self._connected = None
        self._unique_id = unique_id
        
    async def _send(self, data: str):
        LOGGER.debug("sending: " + data)
        if (not self._connected):
            await self.connect()
        await self._device.send(data)
        pass
    
    @property
    def host(self):
        return self._device.ip
    
    @property
    def port(self):
        return self._device.port
    
    @property
    def unique_id(self):
        return self._unique_id
    
    @property
    def is_on(self):
        return self._is_on
    
    async def turn_on(self):
        await self._send("on")
        self._is_on = True
        
    async def turn_off(self):
        await self._send("off")
        self._is_on = False
        
    async def connect(self):
        await self._device.connect()
        self._connected = True
        
    async def disconnect(self):
        await self._device.disconnect()
        self._connected = False