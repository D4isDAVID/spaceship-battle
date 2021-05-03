import pygame
pygame.font.init()


class PlayerEntity:
    FONT = pygame.font.SysFont('Arial', 25)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)
        text = self.FONT.render(self.name, True, self.color)
        surface.blit(text, (
            self.x - text.get_width() // 2,
            self.y - self.radius - text.get_height() - 2
        ))
        text = self.FONT.render(f'{self.hp}/3', True, self.color)
        surface.blit(text, (
            self.x - text.get_width() // 2,
            self.y + text.get_height()
        ))
