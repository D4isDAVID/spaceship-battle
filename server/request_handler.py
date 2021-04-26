from socket import socket, AF_INET, SOCK_STREAM
from json import dumps, loads
from threading import Thread
from lobby import Lobby
from event_handler import EventHandler


class Server:
    def __init__(self):
        self.event_handler = EventHandler(self)
        self.players = {}
        self.lobbies = {0: Lobby()}
    
    def client_thread(self, client, player_id):
        try:
            client.sendall(str(player_id).encode())

            while True:
                data = client.recv(2048).decode()
                events = loads(data)

                if not events:
                    break

                reply = self.event_handler.handle_events(events, player_id)
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
