import pygame
import sys
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from lobby import Lobby
from player import ServerPlayer
from entity.player import PlayerEntity
from entity.bullet import BulletEntity
VERSION = '0.4.4-alpha'


class Server:
    def __init__(self):
        self.players = {}
        self.lobbies = {}

    def client_thread(self, client, player_id):
        client.sendall(f'{player_id}|'.encode())

        while 1:
            try:
                data = client.recv(2048)
                if not data: break
                data = data.decode()
                events = {}

                for i in data.split('|'):
                    event = i.split('-', 1)
                    if event[0] == 'move':
                        event[1] = [bool(int(x)) for x in event[1].split(',')]
                    elif event[0] == 'shoot':
                        event[1] = float(event[1])
                    if event[0]: events[event[0]] = event[1]

                lobby_id = self.players[player_id].lobby_id
                for event, value in events.items():
                    if lobby_id == None:
                        if event == 'join':
                            lobby_id = Lobby.count-1
                            self.players[player_id].lobby_id = lobby_id
                            lobby = self.lobbies[lobby_id]
                            self.players[player_id].entity_id = lobby.entity_count
                            entity_id = self.players[player_id].entity_id
                            lobby.entities[entity_id] = PlayerEntity(value[:16])
                            Thread(target=self.client_send_thread, args=(client, player_id)).start()
                            lobby.entity_count += 1
                            lobby.players += 1
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
            except ConnectionError:
                break
            except Exception as e:
                print(f"Exception | {e}")
                break

        try:
            lobby = self.lobbies[self.players[player_id].lobby_id]
            lobby.entities.pop(self.players[player_id].entity_id)
            lobby.players -= 1
        except Exception:
            pass
        self.players.pop(player_id)
        client.close()
        print(f"Disconnect | Player {player_id}")

    def client_send_thread(self, client, player_id):
        client.sendall(str(self.players[player_id].entity_id).encode())
        lobby = self.lobbies[self.players[player_id].lobby_id]
        clock = pygame.time.Clock()

        while lobby.entities:
            clock.tick(30)
            try:
                if client.fileno() == -1: break
                client.sendall(lobby.serialize().encode())
            except (ConnectionError, OSError):
                continue

    def lobby_thread(self, lobby_id):
        self.lobbies[lobby_id] = Lobby()
        lobby = self.lobbies[lobby_id]
        clock = pygame.time.Clock()
        print('Lobby Running')

        while not lobby.players:
            pass

        while lobby.players:
            delta_time = clock.tick(60) / 1000
            lobby.update(delta_time)
        
        self.lobbies.pop(lobby_id)

    def listen_thread(self, port=7723):
        server = socket(AF_INET, SOCK_STREAM)

        try:
            server.bind(('', port))
            print(f"Server bound to 0.0.0.0:{port}")
            server.listen(1)
        except OSError as e:
            print(f"Exception | {e}")
        else:
            print(f"Server is online. ({VERSION})")

            while 1:
                client, address = server.accept()
                lobby_id = Lobby.count
                player_id = ServerPlayer.count
                if not self.lobbies or self.lobbies[lobby_id-1].players+1 > Lobby.MAX_PLAYERS:
                    lt = Thread(target=self.lobby_thread, args=(lobby_id,))
                    lt.daemon = True
                    lt.start()
                print(f"Connect | Player {player_id}")
                self.players[player_id] = ServerPlayer()
                pt = Thread(
                    target=self.client_thread,
                    args=(client, player_id)
                )
                pt.daemon = True
                pt.start()
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
