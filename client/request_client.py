from socket import socket, AF_INET, SOCK_STREAM
from pickle import dumps, loads
from threading import Thread


class Client:
    def __init__(self, hostname, port=7723):
        self.address = (hostname, port)
        self.socket = socket(AF_INET, SOCK_STREAM)
        self._id = self.connect()

    def connect(self):
        try:
            self.socket.connect(self.address)
            return int(self.socket.recv(1024).decode())
        except OSError as e:
            print(f"[EXCEPTION] {e}")
    
    def send(self, events):
        try:
            self.socket.sendall(dumps(events))
            return loads(self.socket.recv(4096))
        except OSError as e:
            print(f"[EXCEPTION] {e}")
