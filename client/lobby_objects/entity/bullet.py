import pygame


class BulletEntity:
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
