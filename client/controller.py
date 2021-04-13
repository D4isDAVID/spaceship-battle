import pygame


class Controller:
    def __init__(self, network):
        self.network = network

    def move(self):
        keys = pygame.key.get_pressed()

        data = ''
        if keys[pygame.K_LSHIFT]:
            data += 'acc'
        if keys[pygame.K_w]:
            data += 'up'
        if keys[pygame.K_a]:
            data += 'left'
        if keys[pygame.K_s]:
            data += 'down'
        if keys[pygame.K_d]:
            data += 'right'
        
        if data != '':
            self.network.post(data)
