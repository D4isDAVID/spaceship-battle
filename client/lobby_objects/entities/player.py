from client.lobby_objects.entity import Entity
import pygame


class PlayerEntity(Entity):
    FONT = pygame.font.SysFont('Arial', 40)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text = FONT.render(self.name, True, self.color)
        surface.blit(text, (
            self.x + self.width // 2 - text.get_width() // 2,
            self.y - text.get_width() // 2
        ))
