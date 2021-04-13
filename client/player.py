import pygame
pygame.font.init()


class Player:
    FONT = pygame.font.SysFont('Arial', 25)

    def __init__(self, name, x, y, width, height, color):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.velocity = 1
    
    def draw(self, surface):
        rect = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, self.color, rect)
        text = self.FONT.render(self.name, True, self.color)
        surface.blit(text, (self.x + self.width//2 - text.get_width()//2,
                            self.y-50 + self.height//2 - text.get_height()//2))
