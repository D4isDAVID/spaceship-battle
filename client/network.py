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
    
    def get(self):
        try:
            data = {'type': 'get', 'value': None}
            self.socket.sendall(dumps(data))
            return loads(self.socket.recv(4096))
        except OSError as e:
            print('[EXCEPTION]', e)
    
    def post(self, data):
        try:
            data = {'type': 'post', 'value': data}
            self.socket.sendall(dumps(data))
        except OSError as e:
            print('[EXCEPTION]', e)
    
    def auth(self, data):
        try:
            data = {'type': 'auth', 'value': data}
            self.socket.sendall(dumps(data))
            return self.socket.recv(2048).decode()
        except OSError as e:
            print('[EXCEPTION]', e)
