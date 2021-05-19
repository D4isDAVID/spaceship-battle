import random
import time
import math
from threading import Thread


class PlayerEntity:
    SHOT_COOLDOWN = 0.5
    MAX_HP = 4
    RADIUS = 33

    def __init__(self, name):
        self.name = name
        self.rotation = 270
        self.velocity = [0, 0]
        self.move = [False, False, False, False, False]
        self.move_time = 0.0
        self.shoot_time = 0
        self.score = 0
        self.x = 1250
        self.y = 1250
        self.hp = 0
        self.spawning = False
        self.spawn()
    
    def get_distance(self, other):
        if isinstance(other, PlayerEntity):
            if other != self:
                dx = (other.x) - (self.x)
                dy = (other.y) - (self.y)
                return math.sqrt(math.pow(dx,2)+math.pow(dy,2))
        return -1
    
    def spawn_thread(self):
        self.spawning = True
        time.sleep(2.5)
        self.move_time = 0.0
        self.x = random.randint(self.RADIUS, 3500-self.RADIUS)
        self.y = random.randint(self.RADIUS, 3500-self.RADIUS)
        self.rotation = 270
        self.hp = self.MAX_HP
        self.spawning = False
    
    def spawn(self):
        thread = Thread(target=self.spawn_thread)
        thread.daemon = True
        thread.start()
    
    def update(self, delta_time, target_fps):
        if self.hp > 0:
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
            self.validate_position()
            if self.rotation < 0: self.rotation = (360 + self.rotation)
            if self.rotation > 360: self.rotation = (self.rotation - 360)
            if self.shoot_time < self.SHOT_COOLDOWN: self.shoot_time += 0.01 * delta_time * target_fps
        else:
            if self.spawning == False: self.spawn()
    
    def validate_position(self):
        if self.y - self.RADIUS < 0: self.y = self.RADIUS
        elif self.y + self.RADIUS > 3500: self.y = 3500 - self.RADIUS
        if self.x - self.RADIUS < 0: self.x = self.RADIUS
        elif self.x + self.RADIUS > 3500: self.x = 3500 - self.RADIUS
