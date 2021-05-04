import pygame
pygame.font.init()
import os
rocket_red = pygame.transform.scale(pygame.image.load(f'{os.getcwd()}/client/assets/rocket_red.png'), (55, 55))
rocket_blue = pygame.transform.scale(pygame.image.load(f'{os.getcwd()}/client/assets/rocket_blue.png'), (55, 55))

class PlayerEntity:
    FONT = pygame.font.SysFont('Arial', 25)
    BIG_FONT = pygame.font.SysFont('Arial', 50)

    def draw(self, surface, entity):
        width, height = pygame.display.get_window_size()
        x = self.x - entity.x + width/2
        y = self.y - entity.y + height/2
        asset = None
        color = (255, 255, 255)
        if self == entity:
            asset = rocket_blue
            color = (0, 0, 255)
        else:
            asset = rocket_red
            color = (255, 0, 0)
        
        asset = pygame.transform.rotate(asset, -90-self.rotation)
        rect = asset.get_rect(center=asset.get_rect(center=(x, y)).center)

        if self.hp > 0:
            surface.blit(asset, rect)

            text = self.FONT.render(self.name, True, color)
            surface.blit(text, (
                x - text.get_width() // 2,
                y - self.radius - text.get_height() - 3
            ))
            text = self.FONT.render(f'{self.hp}/5', True, color)
            surface.blit(text, (
                x - text.get_width() // 2,
                y + text.get_height() - 3
            ))
        else:
            if self == entity:
                text = self.BIG_FONT.render('Spawning...', True, (255, 255, 255))
                surface.blit(text, (640 - text.get_width() // 2, 240))
    
    def draw_score(self, surface, y):
        text = self.FONT.render(f'{self.score} - {self.name}', True, (255, 255, 255))
        surface.blit(text, (1200 - text.get_width(), 15*y+5*y))
