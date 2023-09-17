import asyncio
import aiohttp

class IpSwitch:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self._is_connected = False
        
    async def connect(self):
        async with aiohttp.ClientSession() as session:
            async with session.get('http://'+self.ip+':'+self.port+'/connect') as response:
                if response.status == 200:
                    self._is_connected = True
                    return True
                else:
                    self._is_connected = False
                    return False
        
    async def disconnect(self):
        async with aiohttp.ClientSession() as session:
            async with session.get('http://'+self.ip+':'+self.port+'/disconnect') as response:
                if response.status == 200:
                    self._is_connected = False
                    return True
                else:
                    self._is_connected = True
                    return False
        
    # create property is connected
    def is_connected(self):
        return self._is_connected 
    
    async def send_data(self, data):
        async with aiohttp.ClientSession() as session:
            async with session.get('http://'+self.ip+':'+self.port+f'/{data}') as response:
                if response.status == 200:
                    return True
                else:
                    return False
    
    async def is_on(self):
        async with aiohttp.ClientSession() as session:
            async with session.get('http://'+self.ip+':'+self.port+'/is_on') as response:
                if response.status == 200:
                    return (await response.json())['is_on']
                else:
                    return False
    
    @staticmethod
    async def discover_devices(ip:str,port:str)->dict:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://'+ip+':'+port+'/get_devices') as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {}