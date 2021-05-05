import random
import time
from threading import Thread
import math


class PlayerEntity:
    def __init__(self, name):
        self.name = name
        self.radius = 30
        self.rotation = 270
        self.velocity = [0, 0]
        self.move = [False, False, False, False, False]
        self.move_time = 0
        self.score = 0
        self.x = 1250
        self.y = 1250
        self.hp = 0
        self.max_hp = 5
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
        self.x = random.randint(0, 2500)
        self.y = random.randint(0, 2500)
        self.hp = self.max_hp
        self.spawning = False
    
    def spawn(self):
        thread = Thread(target=self.spawn_thread)
        thread.daemon = True
        thread.start()
    
    def update(self):
        if self.hp > 0:
            velocity = self.velocity
            if self.move[4]: velocity = [i*1.5 for i in velocity]
            if self.move[0]: self.move_time += 0.06
            if self.move[1]: self.rotation -= 1.5
            if self.move[2]: self.move_time -= 0.06
            if self.move[3]: self.rotation += 1.5
            self.velocity = [
                math.cos(self.rotation / 180 * math.pi) * 2.5,
                math.sin(self.rotation / 180 * math.pi) * 2.5
            ]
            if self.move_time < 0: self.move_time += 0.01
            if self.move_time > 0: self.move_time -= 0.01
            if self.move_time < -1: self.move_time = -1
            if self.move_time > 1: self.move_time = 1
            self.x += velocity[0] * self.move_time
            self.y += velocity[1] * self.move_time
            self.validate_position()
            if self.rotation < 0:
                self.rotation = (360 + self.rotation)
            if self.rotation > 360:
                self.rotation = (self.rotation - 360)
        else:
            if self.spawning == False: self.spawn()
    
    def validate_position(self,):
        if self.y - self.radius < 0: self.y = self.radius
        elif self.y + self.radius > 2500: self.y = 2500 - self.radius
        if self.x - self.radius < 0: self.x = self.radius
        elif self.x + self.radius > 2500: self.x = 2500 - self.radius
