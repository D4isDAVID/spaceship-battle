import pygame


class BulletEntity:
    RADIUS = 5

    def __init__(self, x, y, shooter_id, velocity):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.shooter_id = shooter_id
    
    def draw(self, surface, entity, entity_id):
        width, height = surface.get_size()
        x = self.x - entity.x + width/2
        y = self.y - entity.y + height/2
        color = (255, 0, 0)
        if entity_id == self.shooter_id: color = (0, 0, 255)
        pygame.draw.circle(surface, color, (x, y), self.RADIUS)
        pygame.draw.circle(surface, (255, 255, 255), (x, y), self.RADIUS+1, 1)

    def update(self, delta_time, target_fps):
        self.x += self.velocity[0] * delta_time * target_fps
        self.y += self.velocity[1] * delta_time * target_fps
