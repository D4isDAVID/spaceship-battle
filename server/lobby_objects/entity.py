from abc import abstractmethod


class Entity:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
    
    @abstractmethod
    def update(self):
        pass

    def is_out_of_bounds(self):
        if not (self.x < 0 or self.x + self.width > 3000):
            if not (self.y < 0 or self.y + self.height > 3000):
                return False
        return True
