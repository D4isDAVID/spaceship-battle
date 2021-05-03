import random
import time
from threading import Thread
import math


class PlayerEntity:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.radius = 25
        self.velocity = 2
        self.move = [False, False, False, False, False]
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
        self.x = random.randint(0, 2500)
        self.y = random.randint(0, 2500)
        self.hp = 3
        self.spawning = False
    
    def spawn(self):
        thread = Thread(target=self.spawn_thread)
        thread.daemon = True
        thread.start()
    
    def update(self):
        if self.hp > 0:
            velocity = self.velocity
            if self.move[4]: velocity *= 1.5
            if self.is_moving_in_two_directions(): velocity *= (5/6)
            if self.move[0]: self.y -= velocity
            if self.move[1]: self.x -= velocity
            if self.move[2]: self.y += velocity
            if self.move[3]: self.x += velocity
            self.validate_position()
        else:
            if self.spawning == False: self.spawn()
    
    def is_moving_in_two_directions(self):
        if not (self.move[0] and self.move[2]):
            if not (self.move[1] and self.move[3]):
                if self.move[0] or self.move[2]:
                    if self.move[1] or self.move[3]:
                        return True
        return False
    
    def validate_position(self,):
        if self.y - self.radius < 0: self.y = self.radius
        elif self.y + self.radius > 2500: self.y = 2500 - self.radius
        if self.x - self.radius < 0: self.x = self.radius
        elif self.x + self.radius > 2500: self.x = 2500 - self.radius
