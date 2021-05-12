import pygame


class BulletEntity:
    def draw(self, surface, entity):
        width, height = pygame.display.get_window_size()
        x = self.x - entity.x + width/2
        y = self.y - entity.y + height/2
        if entity == self.entity: self.color = (0, 0, 255)
        else: self.color = (255, 0, 0)
        pygame.draw.circle(surface, (255, 255, 255), (x, y), self.radius+2, 1)
        pygame.draw.circle(surface, self.color, (x, y), self.radius)
