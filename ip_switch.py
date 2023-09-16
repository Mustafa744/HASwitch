import requests
class IpSwitch:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        
    def connect(self):
        res = requests.get('http://'+self.ip+':'+self.port+'/connect')
        if res.status_code == 200:
            self.is_connected = True
            return True
        else:
            self.is_connected = False
            return False
    
    def disconnect(self):
        res = requests.get('http://'+self.ip+':'+self.port+'/disconnect')
        if res.status_code == 200:
            self.is_connected = False
            return True
        else:
            self.is_connected = True
            return False
        
    # create property is connected
    def is_connected(self):
        return self.is_connected 
    
    def send_data(self, data):
        res = requests.get('http://'+self.ip+':'+self.port+f'/{data}')
        if res.status_code == 200:
            return True
        else:
            return False
    
    @staticmethod
    def discover_devices(ip:str,port:str)->dict:
        res = requests.get('http://'+ip+':'+port+'/get_devices')
        if res.status_code == 200:
            # return devices as dict with keys ip , port , name 
            return res.json()
        else:
            return {}