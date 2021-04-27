from client.request_client import Client
import pygame
import math


class Lobby:
    def __init__(self):
        self.entities = []
        self.player = 
    
    def draw(self, surface):
        for entity in self.entities:
            entity.draw(surface)

    def main(self, name, hostname, port=7723):
        window = pygame.display.set_mode((1280, 720))
        clock = pygame.time.Clock()
        client = Client(hostname, port)
        client.send({'join': [0, name]})

        while True:
            clock.tick(60)
            self.draw(window)
            pygame.display.update()

            events = {}
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if not events['move']:
                        events['move'] = [False, False, False, False]
                    if event.key == pygame.K_w: events['move'][0] = True
                    elif event.key == pygame.K_a: events['move'][1] = True
                    elif event.key == pygame.K_s: events['move'][2] = True
                    elif event.key == pygame.K_d: events['move'][3] = True
                elif event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()

                    vector = (
                        mouse_pos[0] - self.player.entity.x,
                        mouse_pos[1] - self.player.entity.y
                    )

                    events['look'] = math.atan2(vector[1], vector[0])
                
            client.send(events)
