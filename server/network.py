from socket import socket, AF_INET, SOCK_STREAM
from pickle import dumps, loads
from threading import Thread
from player import Player


class Network:
    PLAYERS = 6

    def __init__(self):
        self.address = ('localhost', 7723)
        self.players = {}
    
    def client_thread(self, client, player_id):
        # temporary color cause lazy woohoo
        c = ((len(self.players)%self.PLAYERS)+1) * 63
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
                            velocity = player.velocity
                            if 'acc' in data['value']:
                                velocity += velocity/2
                            if 'up' in data['value']:
                                player.y -= velocity
                            if 'left' in data['value']:
                                player.x -= velocity
                            if 'down' in data['value']:
                                player.y += velocity
                            if 'right' in data['value']:
                                player.x += velocity
                        else:
                            player = data['value']
                        if player.y < 0:
                            player.y = 0
                        elif player.y+player.height > 720:
                            player.y = 720-player.height
                        if player.x < 0:
                            player.x = 0
                        elif player.x+player.width > 1280:
                            player.x = 1280-player.width
                    except:
                        pass
                elif data['type'] == 'auth':
                    # another lazy woohoo
                    another_one_has_it = 0
                    done = 0
                    new_name = data['value']

                    while done < 1:
                        for player in self.players:
                            if new_name == self.players[player].name:
                                another_one_has_it += 1
                                new_name = data['value']
                                new_name = f"{new_name} ({another_one_has_it})"
                                done -= 1
                        done += 1
                    
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
            if len(list(self.players.values())) > self.PLAYERS-1:
                c.sendall(">>> TOO MANY PLAYERS <<<".encode())
                c.close()
            else:
                t = Thread(target=self.client_thread, args=(c, player_count))
                t.start()
                player_count += 1

if __name__ == '__main__':
    server = Network()
    thread = Thread(target=server.listen_thread)
    thread.start()
