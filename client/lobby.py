from request_client import Client
import pygame
pygame.font.init()
pygame.mixer.init()
import math
from entity.player import PlayerEntity
import os


class Lobby:
    def __init__(self):
        self.entities = []
        self.entity_id = None
        self.move = [False, False, False, False, False]
    
    def draw(self, surface):
        surface.fill(0)
        e = self.entities[self.entity_id]
        width, height = pygame.display.get_window_size()
        x = -25 - e.x + width/2
        y = -25 - e.y + height/2
        pygame.draw.rect(surface, (225, 225, 225), (x, y, 2525, 25))
        pygame.draw.rect(surface, (225, 225, 225), (x, y, 25, 2525))
        y = 2500 - e.y + height/2
        pygame.draw.rect(surface, (225, 225, 225), (x, y, 2525, 25))
        x = 2500 - e.x + width/2
        y = -25 - e.y + height/2
        pygame.draw.rect(surface, (225, 225, 225), (x, y, 25, 2550))
        surface.blit(pygame.font.SysFont('Arial', 30).render(f'({int(e.x)}, {int(e.y//1)})', True, (255, 255, 255)), (10, 675))
        count = 0
        for entity in list(self.entities.values()):
            if isinstance(entity, PlayerEntity):
                count += 1
                entity.draw_score(surface, count)
            entity.draw(surface, e)

    def main(self, name, hostname, port=7723):
        window = pygame.display.set_mode((1280, 720))
        client = Client(hostname, port)
        self.entity_id = client.send({'join': [0, name]})
        self.entities = client.send({})
        theme = pygame.mixer.music.load(f'{os.getcwd()}/client/assets/theme.ogg')
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

                    pos = [
                        pos[0]-width/2,
                        pos[1]-height/2
                    ]

                    events['shoot'] = math.atan2(pos[1], pos[0]) / math.pi * 180

            self.entities = client.send(events)


if __name__ == '__main__':
    lobby = Lobby()
    ip = input("Enter Server IP: ")
    name = input("Enter Desired Name: ")
    lobby.main(name, ip, 7723)
