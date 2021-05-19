import math
import sys
import pygame
import os
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from background import Background
from entity.player import PlayerEntity
from entity.bullet import BulletEntity
pygame.init()


class Lobby:
    FONT = pygame.font.SysFont('Arial', 25)
    TARGET_FPS = 144

    def __init__(self):
        self.surface = pygame.display.set_mode((1280, 720))
        self.minimap = pygame.Surface((3500, 3500))
        self.background = Background(1250, 1250, (0.1, -0.1))
        self.id = None
        self.entities = {}
        self.entity_id = None
        self.move = [False, False, False, False, False]
        self.assets = {}
        path = os.path.dirname(os.path.realpath( __file__ ))
        self.assets['rocket_red'] = pygame.image.load(os.path.join(path, 'assets', 'rocket_red.png'))
        self.assets['rocket_blue'] = pygame.image.load(os.path.join(path, 'assets', 'rocket_blue.png'))
        self.assets['theme'] = os.path.join(path, 'assets', 'theme.wav')
        self.client = socket(AF_INET, SOCK_STREAM)
    
    def draw(self, delta_time):
        self.surface.fill(0)
        self.minimap.fill(0)
        try:
            e = self.entities[self.entity_id]
        except KeyError:
            pass
        else:
            self.background.update(delta_time, self.TARGET_FPS)
            self.background.draw(self.surface, e)
            width, height = self.surface.get_size()
            border_size = 10
            border_x = border_size - e.x + width/2
            border_y = border_size - e.y + height/2
            border_rect = (border_x, border_y, 3500-border_size*2, 3500-border_size*2)
            pygame.draw.rect(self.surface, (255, 0, 0), border_rect, border_size)
            minimap_size = 200
            pygame.draw.rect(self.minimap, (255, 255, 255), (0, 0, 3485, 3485), 30)
            count = 0
            for entity in self.entities.values():
                if isinstance(entity, PlayerEntity):
                    count += 1
                    color = (255, 0, 0)
                    asset = self.assets['rocket_red']
                    if entity == e:
                        color = (0, 0, 255)
                        asset = self.assets['rocket_blue']
                    entity.draw(self.surface, self.minimap, e, asset, color)
                    entity.draw_score(self.surface, count)
                else:
                    entity.draw(self.surface, e, self.entity_id)
                entity.update(delta_time, self.TARGET_FPS)
            text = self.FONT.render(f'({int(e.x)}, {int(e.y)})', True, (255, 255, 255))
            self.surface.blit(text, (10, 675))
            self.minimap.set_alpha(200)
            self.surface.blit(pygame.transform.scale(self.minimap, (minimap_size, minimap_size)), (15, 15))
    
    def deserialize(self, data):
        deserialized = {}
        data = data.split('||')
        if len(data) > 2 and data[-2]:
            data = data[-2]
        else:
            return
        entities = data.split('|')
        for e in entities:
            i = e.split('-', 1)
            entity_id = int(i[0])
            entity = i[1]
            if entity.count(',') > 4:
                values = entity.split(',', 11)
                move = (values[6], values[7], values[8], values[9], values[10])
                move = tuple(bool(int(i)) for i in move)
                deserialized[entity_id] = PlayerEntity(
                    float(values[0]),
                    float(values[1]),
                    float(values[2]),
                    int(values[3]),
                    int(values[4]),
                    float(values[5]),
                    move,
                    values[11]
                )
            else:
                values = entity.split(',')
                deserialized[entity_id] = BulletEntity(
                    float(values[0]),
                    float(values[1]),
                    int(values[2]),
                    (float(values[3]), float(values[4]))
                )

        self.entities = deserialized

    def get_thread(self):
        try:
            while 1:
                reply = self.client.recv(3072)
                self.deserialize(reply.decode())
        except Exception as e:
            print(f'Exception | {e}')

    def main(self, name, hostname, port=7723):
        try:
            clock = pygame.time.Clock()
            self.client.connect((hostname, port))
            self.id = self.client.recv(1024).decode()
            self.client.sendall(f'join-0,{name}'.encode())
            self.entity_id = int(self.client.recv(1024).decode())
            thread = Thread(target=self.get_thread)
            thread.daemon = True
            thread.start()
            pygame.mixer.music.load(self.assets['theme'])
            volume = 0.5
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(loops=-1)
            version_text = self.FONT.render('0.3.5-alpha_DEV', True, (255, 255, 255))
            running = 1

            while running:
                delta_time = clock.tick(60) / 1000
                self.draw(delta_time)
                self.surface.blit(version_text, (1270-version_text.get_width(), 675))
                fps_text = self.FONT.render(str(delta_time), True, (255, 255, 255))
                self.surface.blit(fps_text, (1270-fps_text.get_width(), 650))
                pygame.display.update()
                
                events = {}
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        running = 0
                        break
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_w: self.move[0] = True
                        elif event.key == pygame.K_a: self.move[1] = True
                        elif event.key == pygame.K_s: self.move[2] = True
                        elif event.key == pygame.K_d: self.move[3] = True
                        elif event.key == pygame.K_LSHIFT: self.move[4] = True
                        events['move'] = self.move
                    elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_w:self.move[0] = False
                        elif event.key == pygame.K_a: self.move[1] = False
                        elif event.key == pygame.K_s: self.move[2] = False
                        elif event.key == pygame.K_d: self.move[3] = False
                        elif event.key == pygame.K_LSHIFT: self.move[4] = False
                        elif event.key == pygame.K_m:
                            if pygame.mixer.music.get_volume() == 0:
                                pygame.mixer.music.set_volume(volume)
                            else:
                                pygame.mixer.music.set_volume(0)
                        elif event.key == pygame.K_EQUALS:
                            volume += 0.05
                            if volume > 1: volume = 1
                            pygame.mixer.music.set_volume(volume)
                        elif event.key == pygame.K_MINUS:
                            volume -= 0.05
                            if volume < 0: volume = 0
                            pygame.mixer.music.set_volume(volume)
                        events['move'] = self.move
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        width, height = pygame.display.get_window_size()
                        pos = [pos[0]-width/2, pos[1]-height/2]
                        events['shoot'] = math.atan2(pos[1], pos[0]) / math.pi * 180

                serialized = ''
                for event, value in events.items():
                    serialized += f'{event}-'
                    if event == 'move':
                        for i in value:
                            serialized += f'{int(i)},'
                        serialized = serialized[:-1]
                    elif event == 'shoot':
                        serialized += str(value)
                    serialized += '|'

                if serialized: self.client.sendall(serialized.encode())
        except OSError as e:
            print(f"Exception | {e}")

if __name__ == '__main__':
    ip = input("Enter Server IP: ")
    name = input("Enter Desired Name: ")
    lobby = Lobby()
    lobby.main(name, ip, 7723)
