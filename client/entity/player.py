import math
import pygame
pygame.init()


class PlayerEntity:
    FONT = pygame.font.SysFont('Arial', 25)
    BIG_FONT = pygame.font.SysFont('Arial', 50)

    def draw(self, surface, minimap, entity, asset, color):
        width, height = surface.get_size()
        x = self.x - entity.x + width/2
        y = self.y - entity.y + height/2
        
        asset_size = self.radius*2 - 2
        asset = pygame.transform.scale(asset, (asset_size, asset_size))
        asset = pygame.transform.rotate(asset, -90 - self.rotation)
        rect = asset.get_rect(center=asset.get_rect(center=(x, y)).center)

        if self.hp > 0:
            surface.blit(asset, rect)
            text = self.FONT.render(self.name, True, color)
            surface.blit(text, (
                x - text.get_width() // 2,
                y - text.get_height() - self.radius * 1.2
            ))
            text = self.FONT.render(f'{self.hp} HP', True, color)
            surface.blit(text, (
                x - text.get_width() // 2,
                y + self.radius * 1.2
            ))
            pygame.draw.circle(minimap, color,
                               (self.x, self.y),
                               self.radius*2.5)
        else:
            if self == entity:
                text = self.BIG_FONT.render('YOU ARE DEAD', True, (255, 0, 0))
                text2 = self.FONT.render('Get ready to spawn...', True, (255, 255, 255))
                surface.blit(text, (640 - text.get_width() // 2, 240))
                surface.blit(text2, (640 - text2.get_width() // 2, 240 + text.get_height()))
    
    def draw_score(self, surface, y):
        text = self.FONT.render(f'{self.score} - {self.name}', True, (255, 255, 255))
        rect = pygame.Surface((text.get_width()+12, text.get_height()+4))
        pygame.draw.rect(rect, (255, 255, 255), (0, 0, rect.get_width(), rect.get_height()))
        rect.set_alpha(50)
        surface.blit(rect, (1255 - rect.get_width()+6, rect.get_height()*y))
        surface.blit(text, (1255 - text.get_width(), text.get_height()*y+4*y))

    def update(self, delta_time, target_fps):
        velocity = self.velocity
        if self.move[4]: velocity = [i*1.5 for i in velocity]
        if self.move[0]: self.move_time += 0.06
        if self.move[1]: self.rotation -= 1.5 * delta_time * target_fps
        if self.move[2]: self.move_time -= 0.06
        if self.move[3]: self.rotation += 1.5 * delta_time * target_fps
        self.velocity = [
            math.cos(self.rotation / 180 * math.pi) * 2.5,
            math.sin(self.rotation / 180 * math.pi) * 2.5
        ]
        if self.move_time < 0: self.move_time += 0.01 * delta_time * target_fps
        if self.move_time > 0: self.move_time -= 0.01 * delta_time * target_fps
        if (-0.01 < self.move_time) and (0.01 > self.move_time):
            self.move_time = 0
        if self.move_time < -1: self.move_time = -1
        if self.move_time > 1: self.move_time = 1
        self.x += velocity[0] * self.move_time * delta_time * target_fps
        self.y += velocity[1] * self.move_time * delta_time * target_fps
        if self.rotation < 0: self.rotation = (360 + self.rotation)
        if self.rotation > 360: self.rotation = (self.rotation - 360)
