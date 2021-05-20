import pygame
import sys
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from lobby import Lobby
from player import ServerPlayer
from entity.player import PlayerEntity
from entity.bullet import BulletEntity


class Server:
    def __init__(self):
        self.players = {}
        self.lobbies = {0: Lobby()}

    def client_thread(self, client, player_id):
        try:
            client.sendall(str(player_id).encode())

            while 1:
                data = client.recv(2048)
                if not data: break
                data = data.decode()
                events = {}
                reply = None

                for i in data.split('|'):
                    event = i.split('-', 1)
                    if event[0] == 'join':
                        event[1] = event[1].split(',', 1)
                        event[1][0] = int(event[1][0])
                    elif event[0] == 'move':
                        event[1] = [bool(int(x)) for x in event[1].split(',')]
                    elif event[0] == 'shoot':
                        event[1] = float(event[1])
                    if event[0]: events[event[0]] = event[1]

                lobby_id = self.players[player_id].lobby_id
                for event, value in events.items():
                    if lobby_id == None:
                        if event == 'join':
                            self.players[player_id].lobby_id = value[0]
                            lobby = self.lobbies[value[0]]
                            if len(value[1]) > 16: value[1] = value[1][:16]
                            self.players[player_id].entity_id = lobby.entity_count
                            lobby.entities[lobby.entity_count] = PlayerEntity(value[1])
                            lobby.players.append(player_id)
                            lobby.entity_count += 1
                            reply = lobby.entity_count - 1
                            Thread(target=self.client_send_thread, args=(client, player_id)).start()
                    else:
                        lobby = self.lobbies[lobby_id]
                        entity_id = self.players[player_id].entity_id
                        entity = lobby.entities[entity_id]
                        if event == 'move':
                            entity.move = value
                        elif event == 'shoot':
                            if entity.hp > 0 and entity.shoot_time >= entity.SHOT_COOLDOWN:
                                lobby.entities[lobby.entity_count] = BulletEntity(entity_id, entity, value)
                                lobby.entity_count += 1
                                entity.shoot_time = 0

                if reply != None: client.sendall(str(reply).encode())
        except Exception as e:
            print(f"Exception | {e}")

        try:
            lobby = self.lobbies[self.players[player_id].lobby_id]
            lobby.entities.pop(self.players[player_id].entity_id)
        except Exception:
            pass
        self.players.pop(player_id)
        client.close()
        print(f"Disconnect | Player {player_id}")

    def client_send_thread(self, client, player_id):
        lobby = self.lobbies[self.players[player_id].lobby_id]
        clock = pygame.time.Clock()

        while lobby.entities:
            clock.tick(lobby.TARGET_FPS)
            if client.fileno() != -1: client.sendall(lobby.serialize().encode())

    def lobby_thread(self, lobby_id):
        lobby = self.lobbies[lobby_id]
        clock = pygame.time.Clock()
        fps = 60
        print('Lobby Running')

        while 1:
            delta_time = clock.tick(60) / 1000
            lobby.update(delta_time)

    def listen_thread(self, port=7723):
        server = socket(AF_INET, SOCK_STREAM)

        try:
            server.bind(('', port))
            print(f"Server bound to 0.0.0.0:{port}")
            server.listen(1)
        except OSError as e:
            print(f"Exception | {e}")
        else:
            print("Server is online. (0.4.2-alpha)")

            lobby = Thread(target=self.lobby_thread, args=(0,))
            lobby.daemon = True
            lobby.start()
            while 1:
                player_id = ServerPlayer.count
                client, address = server.accept()
                print(f"Connect | {address[0]}:{address[1]}")
                self.players[player_id] = ServerPlayer(client)
                thread = Thread(
                    target=self.client_thread,
                    args=(client, player_id)
                )
                thread.daemon = True
                thread.start()
            server.close()


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
            sys.exit()
import pygame
