import math
import copy


class BulletEntity:
    def __init__(self, entity, angle):
        self.entity = entity
        self.original_entity = copy.deepcopy(entity)
        self.x = self.entity.x
        self.y = self.entity.y
        self.radius = 4
        self.color = (255, 255, 255)
        velocity = entity.velocity
        if entity.move[4]: velocity = [v*1.5 for v in velocity]
        self.velocity = [
            math.cos(angle / 180 * math.pi) * 10 + velocity[0] * entity.move_time,
            math.sin(angle / 180 * math.pi) * 10 + velocity[1] * entity.move_time
        ]
    
    def get_distance(self, other):
        dx = (other.x) - (self.x)
        dy = (other.y) - (self.y)
        return math.sqrt(math.pow(dx,2)+math.pow(dy,2))
    
    def update(self, delta_time, target_fps):
        self.x += self.velocity[0] * delta_time * target_fps
        self.y += self.velocity[1] * delta_time * target_fps
    
    def is_out_of_bounds(self):
        if not (self.x - self.radius < 0 or self.x + self.radius > 3500):
            if not (self.y - self.radius < 0 or self.y + self.radius > 3500):
                return False
        return True
