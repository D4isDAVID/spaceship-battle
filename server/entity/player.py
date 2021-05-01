class PlayerEntity:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.x = 500
        self.y = 500
        self.radius = 25
        self.velocity = 2
        self.move = [False, False, False, False, False]
    
    def update(self):
        velocity = self.velocity
        if self.move[4]: velocity *= 1.5
        if self.is_moving_in_two_directions(): velocity *= (5/6)
        if self.move[0]: self.y -= velocity
        if self.move[1]: self.x -= velocity
        if self.move[2]: self.y += velocity
        if self.move[3]: self.x += velocity
        self.validate_position()
    
    def is_moving_in_two_directions(self):
        if not (self.move[0] and self.move[2]):
            if not (self.move[1] and self.move[3]):
                if self.move[0] or self.move[2]:
                    if self.move[1] or self.move[3]:
                        return True
        return False
    
    def validate_position(self):
        if self.y - self.radius < 0: self.y = self.radius
        elif self.y + self.radius > 720: self.y = 720 - self.radius
        if self.x - self.radius < 0: self.x = self.radius
        elif self.x + self.radius > 1280: self.x = 1280 - self.radius
