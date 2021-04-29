import pygame


class BulletEntity:
    def draw(self, surface):
        rect = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, self.color, rect)
