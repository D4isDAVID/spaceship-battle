import pygame
from socket import socket, AF_INET, SOCK_STREAM
from pickle import dumps, loads
from threading import Thread
from lobby import Lobby
from event_handler import EventHandler
from player import ServerPlayer


class Server:
    def __init__(self):
        self.event_handler = EventHandler(self)
        self.players = {}
        self.lobbies = {0: Lobby()}
    
    def client_thread(self, client, player_id):
        try:
            client.sendall(str(player_id).encode())

            while True:
                data = client.recv(2048)

                if not data:
                    break

                events = loads(data)

                reply = self.event_handler.handle_events(events, player_id)
                client.sendall(dumps(reply))
        except OSError as e:
            print(f"[EXCEPTION] {e}")
        
        lobby = self.lobbies[self.players[player_id].lobby_id]
        lobby.entities.pop(self.players[player_id].entity_id)
        self.players.pop(player_id)
        client.close()
        print(f"[DISCONNECTED] Player {player_id}")
    
    def lobby_thread(self, lobby_id):
        lobby = self.lobbies[lobby_id]
        lobby.main()
    
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
        lobby = Thread(target=self.lobby_thread, args=(0, ))
        lobby.daemon = True
        lobby.start()
        while True:
            client, address = server.accept()
            print(f"[CONNECTION] From {address[0]}:{address[1]}")
            self.players[player_count] = ServerPlayer()
            thread = Thread(
                target=self.client_thread,
                args=(client, player_count)
            )
            thread.daemon = True
            thread.start()
            player_count += 1
        

if __name__ == '__main__':
    server = Server()
    thread = Thread(target=server.listen_thread)
    thread.daemon = True
    thread.start()
    print("Type 'stop' to stop the server.")
    while True:
        command = input()
        if command == 'stop':
            pygame.quit()
            exit()
