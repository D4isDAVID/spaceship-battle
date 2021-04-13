import threading
from socket import socket, AF_INET, SOCK_STREAM
from pickle import dumps, loads
from threading import Thread
from player import Player


class Network:
    PLAYERS = 6

    def __init__(self):
        self.address = ('', 7723)
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
                data = loads(client.recvfrom(2048)[0])
                reply = None

                if not data:
                    break

                if 'get' in data:
                    reply = dumps(list(self.players.values()))
                elif 'post' in data:
                    if 'move' in data['post']:
                        player.move(data['post']['move'])
                    reply = dumps(list(self.players.values()))
                elif 'auth' in data:
                    old_name = data['auth']
                    has_it = 0
                    done = 0
                    new_name = old_name

                    if new_name == '':
                        reply = [None]
                    else:
                        while done < 1:
                            for player in self.players:
                                if new_name == self.players[player].name:
                                    has_it += 1
                                    new_name = old_name
                                    new_name = f"{new_name} ({has_it})"
                                    done -= 1
                            done += 1
                        
                        reply = [new_name]
                        self.players[player_id] = Player(new_name, 640, 360, 50, 50, (c, 128, c))
                        print(f"[JOINED] Player {player_id} - {new_name}")
                    reply = dumps(reply)
                client.sendall(reply)
            except Exception as e:
                if str(e) != 'Ran out of input':
                    print(f"[EXCEPTION] Player {player_id} - {e}")
                break
        
        try:
            self.players.pop(player_id)
        except:
            print(f"Player {player_id} disconnected without joining the game")
        client.close()
        print(f"[DISCONNECTED] Player {player_id}")

    def listen_thread(self):
        server = socket(AF_INET, SOCK_STREAM)

        try:
            server.bind(self.address)
        except OSError as e:
            print(f"[EXCEPTION] {e}")
        
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
                t.daemon = True
                t.start()
                player_count += 1

if __name__ == '__main__':
    server = Network()
    thread = Thread(target=server.listen_thread)
    thread.daemon = True
    thread.start()
    while True:
        var = input()
        if var == 'stop':
            exit()
