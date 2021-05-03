import pygame
pygame.font.init()


class PlayerEntity:
    FONT = pygame.font.SysFont('Arial', 25)

    def draw(self, surface, entity):
        width, height = pygame.display.get_window_size()
        x = self.x - entity.x + width/2
        y = self.y - entity.y + height/2

        pygame.draw.circle(surface, self.color, (x, y), self.radius)
        text = self.FONT.render(self.name, True, self.color)
        surface.blit(text, (
            x - text.get_width() // 2,
            y - self.radius - text.get_height() - 2
        ))
        text = self.FONT.render(f'{self.hp}/3', True, self.color)
        surface.blit(text, (
            x - text.get_width() // 2,
            y + text.get_height() - 2
        ))
