from socket import socket, AF_INET, SOCK_STREAM
from json import dumps, loads
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
            self.socket.sendall(dumps(events).encode())
            return loads(self.socket.recv(2048).decode())
        except OSError as e:
            print(f"[EXCEPTION] {e}")


if __name__ == '__main__':
    client = Client('127.0.0.1')
    h = 0
    while True:
        d = {}
        try:
            h = int(input('How many '))
        except:
            h = 1
        for i in range(h):
            t = input('Enter Event')
            v = input('Enter Value')
            d[t] = v

        print(client.send(d))
