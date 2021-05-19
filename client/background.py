import pygame
import os
loc = os.path.dirname(os.path.realpath(__file__))
asset = os.path.join(loc, 'assets', 'bg.png')
asset = pygame.image.load(asset)


class Background:
    def __init__(self, x, y, velocity):
        self.width = 1280
        self.height = 720
        self.x = x - self.width/2
        self.y = y - self.height/2
        self.asset = pygame.transform.scale(asset, (self.width, self.height))
        self.velocity = velocity
        self.surface = pygame.Surface((self.width*3, self.height*3))
        for x in range(3):
            for y in range(3):
                self.surface.blit(asset, (self.width*(x), self.height*(y)))
    
    def update(self, delta_time, target_fps):
        self.x -= self.velocity[0] * delta_time * target_fps
        self.y -= self.velocity[1] * delta_time * target_fps

    def draw(self, surface, entity):
        width, height = pygame.display.get_window_size()
        if self.x+self.width > entity.x:
            self.x -= self.width
        elif self.x+self.width*2 < entity.x:
            self.x += self.width
        if self.y+self.height > entity.y:
            self.y -= self.height
        elif self.y+self.height*2 < entity.y:
            self.y += self.height
        x = self.x - entity.x + width/2
        y = self.y - entity.y + height/2
        surface.blit(self.surface, (x, y))
