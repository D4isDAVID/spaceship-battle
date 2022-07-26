import math
import copy


class BulletEntity:
    RADIUS = 5

    def __init__(self, shooter_id, shooter, angle):
        self.shooter_id = shooter_id
        self.shooter = shooter
        self.original_shooter = copy.deepcopy(shooter)
        self.x = self.shooter.x
        self.y = self.shooter.y
        velocity = shooter.velocity
        if shooter.move[4]: velocity = [v*1.5 for v in velocity]
        self.velocity = [
            math.cos(angle / 180 * math.pi) * 10 + velocity[0] * shooter.move_time,
            math.sin(angle / 180 * math.pi) * 10 + velocity[1] * shooter.move_time
        ]

    def get_distance(self, other):
        dx = (other.x) - (self.x)
        dy = (other.y) - (self.y)
        return math.sqrt(math.pow(dx,2)+math.pow(dy,2))

    def update(self, delta_time, target_fps):
        self.x += self.velocity[0] * delta_time * target_fps
        self.y += self.velocity[1] * delta_time * target_fps

    def is_out_of_bounds(self):
        if not (self.x - self.RADIUS < 0 or self.x + self.RADIUS > 3500):
            if not (self.y - self.RADIUS < 0 or self.y + self.RADIUS > 3500):
                return False
        return True
