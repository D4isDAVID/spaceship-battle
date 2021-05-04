import pygame
pygame.font.init()
import os
rocket_red = pygame.image.load(f'{os.getcwd()}/client/entity/assets/rocket_red.png')
rocket_blue = pygame.image.load(f'{os.getcwd()}/client/entity/assets/rocket_blue.png')

class PlayerEntity:
    FONT = pygame.font.SysFont('Arial', 25)
    BIG_FONT = pygame.font.SysFont('Arial', 50)

    def draw(self, surface, entity):
        width, height = pygame.display.get_window_size()
        x = self.x - entity.x + width/2
        y = self.y - entity.y + height/2
        rotation = -90 - self.rotation
        asset = None
        color = (255, 255, 255)
        if self == entity:
            asset = rocket_blue
            color = (0, 0, 255)
        else:
            asset = rocket_red
            color = (255, 0, 0)
        asset = pygame.transform.rotate(asset, rotation)
        size = self.rotation%45 * ()
        print(size)
        asset = pygame.transform.scale(asset, (int(self.radius*2+size), int(self.radius*2+size)))

        if self.hp > 0:
            pygame.draw.circle(surface, color, (x, y), self.radius)
            surface.blit(asset, (x-self.radius-size//2,y-self.radius-size//2))

            text = self.FONT.render(self.name, True, color)
            surface.blit(text, (
                x - text.get_width() // 2,
                y - self.radius - text.get_height() - 2
            ))
            text = self.FONT.render(f'{self.hp}/5', True, color)
            surface.blit(text, (
                x - text.get_width() // 2,
                y + text.get_height() - 2
            ))
        else:
            if self == entity:
                text = self.BIG_FONT.render('Spawning...', True, (255, 255, 255))
                surface.blit(text, (
                    640 - text.get_width() // 2,
                    240
                ))
    
    def draw_score(self, surface, y):
        text = self.FONT.render(f'{self.score} - {self.name}', True, (255, 255, 255))
        surface.blit(text, (1200 - text.get_width(), 15*y+5*y))
