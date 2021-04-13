class Player:
    def __init__(self, name, x, y, width, height, color):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.velocity = 5
    
    def move(self, data):
        velocity = self.velocity
        if 'acc' in data:
            velocity += velocity/2
        if 'up' in data:
            self.y -= velocity
        if 'left' in data:
            self.x -= velocity
        if 'down' in data:
            self.y += velocity
        if 'right' in data:
            self.x += velocity
        self.validate_position()
    
    def validate_position(self):
        if self.y < 0:
            self.y = 0
        elif self.y + self.height > 720:
            self.y = 720 - self.height
        if self.x < 0:
            self.x = 0
        elif self.x + self.width > 1280:
            self.x = 1280 - self.width
