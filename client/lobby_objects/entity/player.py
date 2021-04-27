import pygame
pygame.font.init()


class PlayerEntity:
    FONT = pygame.font.SysFont('Arial', 30)

    def draw(self, surface):
        rect = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, self.color, rect)
        text = self.FONT.render(self.name, True, self.color)
        surface.blit(text, (
            self.x + self.width // 2 - text.get_width() // 2,
            self.y - text.get_width() // 2
        ))
