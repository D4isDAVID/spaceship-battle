import math
from entity.player import PlayerEntity


class BulletEntity:
    def __init__(self, entity, angle):
        self.entity = entity
        self.x = self.entity.x
        self.y = self.entity.y
        self.radius = 2.5
        self.color = (255, 255, 255)
        self.velocity = [
            math.cos(angle / 180 * math.pi) * 12,
            math.sin(angle / 180 * math.pi) * 12
        ]
    
    def get_distance(self, other):
        if isinstance(other, PlayerEntity):
            if other != self.entity:
                dx = (other.x) - (self.x)
                dy = (other.y) - (self.y)
                return math.sqrt(math.pow(dx,2)+math.pow(dy,2))
        return -1
    
    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
    
    def is_out_of_bounds(self):
        if not (self.x < 0 or self.x + self.radius > 1280):
            if not (self.y < 0 or self.y + self.radius > 720):
                return False
        return True
