import math
import pygame
import os
from request_client import Client
from entity.player import PlayerEntity
pygame.font.init()
pygame.mixer.init()


class Lobby:
    FONT = pygame.font.SysFont('Arial', 30)

    def __init__(self):
        self.entities = []
        self.entity_id = None
        self.move = [False, False, False, False, False]
    
    def draw(self, surface):
        surface.fill(0)
        e = self.entities[self.entity_id]
        width, height = pygame.display.get_window_size()
        block_size = 100
        for i in range(0, 2500, block_size):
            for j in range(0, 2500, block_size):
                x = i - e.x + width/2
                y = j - e.y + height/2
                rect = pygame.Rect(x, y, block_size, block_size)
                pygame.draw.rect(surface, (35, 35, 35), rect, 1)
        border_size = 10
        x = -border_size/2 - e.x + width/2
        y = -border_size/2 - e.y + height/2
        rect = (x, y, 2500+border_size, 2500+border_size)
        pygame.draw.rect(surface, (255, 0, 0), rect, border_size)
        text = f'({int(e.x)}, {int(e.y)})'
        text = self.FONT.render(text, True, (255, 255, 255))
        surface.blit(text, (10, 675))
        text = self.FONT.render('0.3.1-alpha', True, (255, 255, 255))
        surface.blit(text, (1270-text.get_width(), 675))
        minimap_size = 200
        minimap = pygame.Surface((2600, 2600))
        pygame.draw.rect(minimap, (255, 255, 255), (0, 0, 2600, 2600), 50)
        count = 0
        for entity_id, entity in self.entities.items():
            if isinstance(entity, PlayerEntity):
                count += 1
                entity.draw_score(surface, count)
                if entity.hp > 0:
                    if entity_id == self.entity_id:
                        pygame.draw.circle(minimap, (0, 0, 255), (entity.x+50, entity.y+50), entity.radius)
                    else:
                        pygame.draw.circle(minimap, (255, 0, 0), (entity.x+50, entity.y+50), entity.radius)
            entity.draw(surface, e)
        minimap.set_alpha(200)
        surface.blit(pygame.transform.scale(minimap, (minimap_size, minimap_size)), (15, 15))

    def main(self, name, hostname, port=7723):
        window = pygame.display.set_mode((1280, 720))
        client = Client(hostname, port)
        self.entity_id = client.send({'join': [0, name]})
        self.entities = client.send({})
        loc = os.path.dirname(os.path.realpath( __file__ ))
        theme = os.path.join(loc, 'assets', 'theme.wav')
        theme = pygame.mixer.music.load(theme)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(loops=-1)

        while True:
            self.draw(window)
            pygame.display.update()

            events = {}
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
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
                            pygame.mixer.music.set_volume(0.3)
                        else:
                            pygame.mixer.music.set_volume(0)
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
