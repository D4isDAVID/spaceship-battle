from socket import socket, AF_INET, SOCK_STREAM
from json import dumps, loads
from threading import Thread


class Server:
    def __init__(self):
        self.players = {}
        self.lobbies = {}
    
    def client_thread(self, client, player_id):
        try:
            client.sendall(str(player_id).encode())

            while True:
                data = client.recv(2048).decode()
                events = loads(data)

                if not events:
                    break

                reply = events
                client.sendall(dumps(reply).encode())
        except OSError as e:
            print(f"[EXCEPTION] {e}")
        
        self.players.pop(player_id)
        client.close()
        print(f"[DISCONNECTED] Player {player_id}")
    
    def listen_thread(self, port=7723):
        server = socket(AF_INET, SOCK_STREAM)

        try:
            print(f"Binding server to 127.0.0.1:{port}")
            server.bind(('', port))
        except OSError as e:
            print(f"[EXCEPTION], {e}")
        
        server.listen(1)
        print("Server is online.")

        player_count = 0
        while True:
            client, address = server.accept()
            print("[CONNECTION] From {address[0]}:{address[1]}")
            self.players[player_count] = 'yeah' # Player()
            thread = Thread(
                target=self.client_thread,
                args=(client, player_count)
            )
            thread.daemon = True
            thread.start()


if __name__ == '__main__':
    server = Server()
    thread = Thread(target=server.listen_thread)
    thread.daemon = True
    thread.start()
    while True:
        command = input()
        if command == 'stop':
            exit()
