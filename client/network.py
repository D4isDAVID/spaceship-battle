from socket import socket, AF_INET, SOCK_STREAM
from pickle import dumps, loads


class Network:
    def __init__(self, hostname):
        self.address = (hostname, 7723)
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.__id = self.connect()
    
    @property
    def id(self):
        return self.__id
    
    def connect(self):
        try:
            self.socket.connect(self.address)
            return int(self.socket.recv(1024).decode())
        except OSError as e:
            print('[EXCEPTION]', e)
        
    def send(self, type, data):
        try:
            request = {type: data}
            self.socket.sendall(dumps(request))
            return loads(self.socket.recv(2048))
        except OSError as e:
            print('[EXCEPTION]', e)
    
    def get(self):
        return self.send('get', None)
    
    def post(self, data):
        return self.send('post', data)
    
    def auth(self, data):
        reply = self.send('auth', data)
        return reply[0]
