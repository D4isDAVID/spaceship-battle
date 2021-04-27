from server.lobby_objects.entity import Entity


class PlayerEntity(Entity):
    def __init__(self, name, color):
        self.name = name
        self.x = 500
        self.y = 500
        self.width = 50
        self.height = 50
        self.color = color
        self.velocity = 1
        self.accelerate = False
        self.move = [False, False, False, False]
        self.angle = 0
    
    def update(self):
        velocity = self.velocity
        if self.accelerate: velocity *= 1.5
        if self.is_moving_in_two_directions(): velocity *= (5/6)
        if move[0]: self.y -= velocity
        if move[1]: self.x -= velocity
        if move[2]: self.y += velocity
        if move[3]: self.x += velocity
    
    def is_moving_in_two_directions(self):
        if not (self.move[0] and self.move[2]):
            if not (self.move[1] and self.move[3]):
                if self.move[0] or self.move[2]:
                    if self.move[1] or self.move[3]:
                        return True
        return False
