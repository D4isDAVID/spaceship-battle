from client.lobby_objects.entity import Entity
import pygame


class BulletEntity(Entity):
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
