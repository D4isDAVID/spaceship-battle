class PlayerEntity:
    def __init__(self, name, color, player_id):
        self.name = name
        self.color = color
        self.player_id = player_id
        self.x = 500
        self.y = 500
        self.width = 50
        self.height = 50
        self.velocity = 3
        self.move = [False, False, False, False, False]
        self.angle = 0
    
    def update(self):
        velocity = self.velocity
        if self.move[4]: velocity *= 1.5
        if self.is_moving_in_two_directions(): velocity *= (5/6)
        if self.move[0]: self.y -= velocity
        if self.move[1]: self.x -= velocity
        if self.move[2]: self.y += velocity
        if self.move[3]: self.x += velocity
    
    def is_moving_in_two_directions(self):
        if not (self.move[0] and self.move[2]):
            if not (self.move[1] and self.move[3]):
                if self.move[0] or self.move[2]:
                    if self.move[1] or self.move[3]:
                        return True
        return False
    
    def is_out_of_bounds(self):
        if not (self.x < 0 or self.x + self.width > 5000):
            if not (self.y < 0 or self.y + self.height > 5000):
                return False
        return True
