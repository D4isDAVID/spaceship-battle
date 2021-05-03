import random
import time
from threading import Thread


class PlayerEntity:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.radius = 25
        self.velocity = 2
        self.move = [False, False, False, False, False]
        self.score = 0
        self.x = -50
        self.y = -50
        self.hp = 0
        self.alive = False
        self.spawning = False
        self.spawn()
    
    def spawn_thread(self):
        time.sleep(2.5)
        self.hp = 3
        self.alive = True
        self.x = random.randint(0, 2500)
        self.y = random.randint(0, 2500)
        self.spawning = False
        print(self.x, self.y)
    
    def spawn(self):
        self.spawning = True
        thread = Thread(target=self.spawn_thread)
        thread.daemon = True
        thread.start()
    
    def update(self):
        if self.alive:
            if self.hp <= 0:
                self.alive = False
            velocity = self.velocity
            if self.move[4]: velocity *= 1.5
            if self.is_moving_in_two_directions(): velocity *= (5/6)
            if self.move[0]: self.y -= velocity
            if self.move[1]: self.x -= velocity
            if self.move[2]: self.y += velocity
            if self.move[3]: self.x += velocity
            self.validate_position()
        else:
            self.x = -50
            self.y = -50
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
