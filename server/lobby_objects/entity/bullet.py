import math


class BulletEntity:
    def __init__(self, entity, angle):
        self.entity = entity
        self.x = self.entity.x - self.entity.width // 2
        self.y = self.entity.y - self.entity.height // 2
        self.width = 5
        self.height = 5
        self.velocity = [
            math.sin(angle // 180 * math.pi) + 5,
            math.cos(angle // 180 * math.pi) + 5
        ]
    
    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
    
    def is_out_of_bounds(self):
        if not (self.x < 0 or self.x + self.width > 5000):
            if not (self.y < 0 or self.y + self.height > 5000):
                return False
        return True
