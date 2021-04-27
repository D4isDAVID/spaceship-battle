from abc import abstractmethod


class Entity:
    def __init__(self, x, y, width, height, color):
        self.rect = (x, y, width, height)
        self.color = color
    
    @abstractmethod
    def draw(self):
        pass
