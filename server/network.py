from socket import socket, AF_INET, SOCK_STREAM
from pickle import dumps, loads
from threading import Thread
from player import Player


class Network:
    PLAYERS = 4

    def __init__(self):
        self.address = ('localhost', 7723)
        self.players = {}
    
    def client_thread(self, client, player_id):
        # temporary color cause lazy woohoo
        c = ((len(self.players)%4)+1) * 63
        client.sendall(str(player_id).encode('utf-8'))

        while True:
            try:
                try:
                    player = self.players[player_id]
                except:
                    pass
                data = loads(client.recv(4096))

                print(f"[RECIEVED] {data['type']} {data['value']}")

                if not data:
                    break

                if data['type'] == 'get':
                    client.sendall(dumps(list(self.players.values())))
                    print(f"[SENT] {self.players}")
                elif data['type'] == 'post':
                    try:
                        if isinstance(data['value'], str):
                            if 'acc' in data['value']:
                                player.velocity *= 2
                            if 'up' in data['value']:
                                player.y -= player.velocity
                            if 'left' in data['value']:
                                player.x -= player.velocity
                            if 'down' in data['value']:
                                player.y += player.velocity
                            if 'right' in data['value']:
                                player.x += player.velocity
                            player.velocity /= self.players[player_id].velocity
                        else:
                            player = data['value']
                        if player.y < 0:
                            player.y = 0
                        elif player.y > 720:
                            player.y = 720
                        if player.x < 0:
                            player.x = 0
                        elif player.x > 1280:
                            player.x = 1280
                        self.players[player_id] = player
                    except:
                        pass
                elif data['type'] == 'auth':
                    another_one_has_it = 0
                    done = 0
                    new_name = ''

                    while done >= 1:
                        for player in self.players:
                            if data['value'] == player.name:
                                ++another_one_has_it
                                --done
                        ++done
                    
                    if another_one_has_it > 0:
                        new_name = f"{data['value']} ({another_one_has_it})"
                    else:
                        new_name = data['value']
                    client.sendall(new_name.encode('utf-8'))
                    self.players[player_id] = Player(new_name, 640, 360, 50, 50, (c, 128, c))
                    print(f"[SENT] {new_name}")
            except Exception as e:
                print('[EXCEPTION]', player_id, e)
                break
        
        self.players.pop(player_id)
        client.close()
        print('[DISCONNECTED]', player_id)

    def listen_thread(self):
        server = socket(AF_INET, SOCK_STREAM)

        try:
            server.bind(self.address)
        except OSError as e:
            print('[EXCEPTION]', e)
        
        server.listen(1)
        print("Listening to port", self.address[1])

        player_count = 0

        while True:
            c, addr = server.accept()
            print(f"[CONNECTION] {addr[0]}:{addr[1]}")
            if len(list(self.players.values())) > self.PLAYERS:
                c.close()
            else:
                t = Thread(target=self.client_thread, args=(c, player_count))
                t.start()
                player_count += 1

if __name__ == '__main__':
    server = Network()
    thread = Thread(target=server.listen_thread)
    thread.start()
