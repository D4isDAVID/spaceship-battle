from pygame.time import Clock


class Lobby:
    PLAYER_MAX = 16
    MAX_PLAYERS = 8

    def __init__(self):
        self.players = {}
        self.entities = {}
    
    def update(self):
        for entity in self.entities:
            entity.update()

    def main(self):
        clock = Clock()
        print('Lobby Running')

        while True:
            clock.tick(60)
            self.update()
