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
        self.velocity = 3
    
    def drawentity(self, surface):
        rect = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, self.color, rect)
    
    def text_on_head(self, surface, t):
        text = self.FONT.render(t, True, self.color)
        surface.blit(text, (self.x + self.width//2 - text.get_width()//2,
                            50+self.y + self.height//2 - text.get_height()//2))
    
    def draw(self, surface):
        self.drawentity(surface)
        self.text_on_head(surface, self.name)
