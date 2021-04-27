from server.lobby_objects.entity import Entity
import math


class BulletEntity(Entity):
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
