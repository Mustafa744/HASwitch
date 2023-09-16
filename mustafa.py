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

# class GodoxInstance:
#     def __init__(self, ip, unique_id: str) -> None:
#         self._ip = ip
#         self._device = BleakClient(self._mac)
#         self._is_on = None
#         self._connected = None
#         self._brightness = None
#         self._unique_id = unique_id

#     async def _send(self, data: bytearray):
#         LOGGER.debug(''.join(format(x, ' 03x') for x in data))
        
#         if (not self._connected):
#             await self.connect()
        
#         crcinst = Crc8Maxim()
#         crcinst.process(data)
#         await self._device.write_gatt_char(WRITE_UUID, data + crcinst.finalbytes())

#     @property
#     def mac(self):
#         return self._mac

#     @property
#     def unique_id(self):
#         return self._unique_id
#     @property
#     def is_on(self):
#         return self._is_on

#     @property
#     def brightness(self):
#         return self._brightness

#     async def set_brightness(self, intensity: int):
#         header = bytes.fromhex("f0d10501")
#         command = bytes([intensity])
#         params = bytes.fromhex("380c01")

#         await self._send(header + command + params)

#         self._brightness = intensity

#     async def turn_on(self):
#         header = bytes.fromhex("f0d0060c")
#         command = bytes.fromhex("01")
#         params = bytes.fromhex("00000000")

#         await self._send(header + command + params)
#         self._is_on = True

#     async def turn_off(self):
#         header = bytes.fromhex("f0d0060c")
#         command = bytes.fromhex("00")
#         params = bytes.fromhex("00000000")

#         await self._send(header + command + params)
#         self._is_on = False

#     async def connect(self):
#         await self._device.connect(timeout=20)
#         await asyncio.sleep(1)
#         self._connected = True

#     async def disconnect(self):
#         if self._device.is_connected:
#             await self._device.disconnect()            
            
class MustafaInstance:
    def __init__(self,ip:str,port:str,unique_id:str) -> None:
        self._ip = ip
        self._port = port
        self._device = IpSwitch(self.ip,self.port)
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
    def ip(self):
        return self._ip
    
    @property
    def port(self):
        return self._port
    
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