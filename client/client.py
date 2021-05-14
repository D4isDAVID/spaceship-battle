import math
import pygame
import os
from request_client import Client
from entity.player import PlayerEntity
from background import Background
pygame.font.init()
pygame.mixer.init()


class Lobby:
    FONT = pygame.font.SysFont('Arial', 25)

    def __init__(self):
        self.entities = {}
        self.entity_id = None
        self.move = [False, False, False, False, False]
    
    def draw(self, surface, minimap, background):
        surface.fill(0)
        minimap.fill(0)
        e = self.entities[self.entity_id]
        background.update()
        background.draw(surface, e)
        width, height = pygame.display.get_window_size()
        border_size = 10
        border_x = -border_size/2 - e.x + width/2
        border_y = -border_size/2 - e.y + height/2
        border_rect = (border_x, border_y, 3500+border_size, 3500+border_size)
        pygame.draw.rect(surface, (255, 0, 0), border_rect, border_size)
        minimap_size = 200
        pygame.draw.rect(minimap, (255, 255, 255), (0, 0, 3475, 3475), 50)
        count = 0
        for entity in self.entities.values():
            if isinstance(entity, PlayerEntity):
                count += 1
                entity.draw_score(surface, count)
                entity.draw(surface, minimap, e)
            else:
                entity.draw(surface, e)
        text = self.FONT.render(f'({int(e.x)}, {int(e.y)})', True, (255, 255, 255))
        surface.blit(text, (10, 675))
        text = self.FONT.render('client 0.3.2-alpha', True, (255, 255, 255))
        surface.blit(text, (1270-text.get_width(), 675))
        minimap.set_alpha(200)
        surface.blit(pygame.transform.scale(minimap, (minimap_size, minimap_size)), (15, 15))

    def main(self, name, hostname, port=7723):
        window = pygame.display.set_mode((1280, 720))
        minimap = pygame.Surface((3500, 3500))
        client = Client(hostname, port)
        self.entity_id = client.send({'join': [0, name]})
        self.entities = client.send({})
        e = self.entities[self.entity_id]
        background = Background(e.x, e.y, (0.1, -0.1))
        loc = os.path.dirname(os.path.realpath( __file__ ))
        theme = os.path.join(loc, 'assets', 'theme.wav')
        volume = 0.3
        theme = pygame.mixer.music.load(theme)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loops=-1)

        while True:
            self.draw(window, minimap, background)
            pygame.display.update()

            events = {}
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
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

            self.entities = client.send(events)

if __name__ == '__main__':
    lobby = Lobby()
    ip = input("Enter Server IP: ")
    name = input("Enter Desired Name: ")
    lobby.main(name, ip, 7723)
