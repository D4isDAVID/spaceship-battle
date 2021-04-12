import pygame


class Controller:
    def __init__(self, network):
        self.network = network

    def move(self):
        keys = pygame.key.get_pressed()

        data = ''
        if keys[pygame.K_SPACE]:
            data += 'acc'
        if keys[pygame.K_UP]:
            data += 'up'
        if keys[pygame.K_LEFT]:
            data += 'left'
        if keys[pygame.K_DOWN]:
            data += 'down'
        if keys[pygame.K_RIGHT]:
            data += 'right'
        
        if data != '':
            self.network.post(data)
