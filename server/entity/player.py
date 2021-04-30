class PlayerEntity:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.x = 500
        self.y = 500
        self.width = 50
        self.height = 50
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
        if self.y < 0: self.y = 0
        elif self.y + self.height > 720: self.y = 720 - self.height
        if self.x < 0: self.x = 0
        elif self.x + self.width > 1280: self.x = 1280 - self.width
    
    def is_out_of_bounds(self):
        if not (self.x < 0 or self.x + self.width > 1280):
            if not (self.y < 0 or self.y + self.height > 720):
                return False
        return True
