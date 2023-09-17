import requests
from homeassistant.core import HomeAssistant
class IpSwitch:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self._is_connected = False
        self.hass = HomeAssistant
        
    def connect_handler(self):
        res = requests.get('http://'+self.ip+':'+self.port+'/connect')
        if res.status_code == 200:
            self._is_connected = True
            return True
        else:
            self._is_connected = False
            return False
    async def connect(self):
        return await self.hass.async_add_executor_job(self.connect_handler)
    
    def disconnect(self):
        res = requests.get('http://'+self.ip+':'+self.port+'/disconnect')
        if res.status_code == 200:
            self._is_connected = False
            return True
        else:
            self._is_connected = True
            return False
        
    # create property is connected
    def is_connected(self):
        return self._is_connected 
    
    def send_data(self, data):
        res = requests.get('http://'+self.ip+':'+self.port+f'/{data}')
        if res.status_code == 200:
            return True
        else:
            return False
    
    def is_on(self):
        res = requests.get('http://'+self.ip+':'+self.port+'/is_on')
        if res.status_code == 200:
            return res.json()['is_on']
        else:
            return False
    # def turn_on(self):
    #     return self.send_data('on')
    
    # def turn_off(self):
    #     return self.send_data('off')
    
    @staticmethod
    def discover_devices(ip:str,port:str)->dict:
        res = requests.get('http://'+ip+':'+port+'/get_devices')
        if res.status_code == 200:
            # return devices as dict with keys ip , port , name 
            return res.json()
        else:
            return {}