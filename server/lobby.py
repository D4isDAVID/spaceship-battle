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
                # move = self.players[entity.id].move
                # velocity = entity.velocity
                # if entity.accelerate: velocity *= 1.5
                # if move[0]: entity.y -= velocity
                # if move[1]: entity.y -= velocity
                # if move[2]: entity.y -= velocity
                # if move[3]: entity.y -= velocity

                # entity.y += entity.velocity[0]
                # entity.x += entity.velocity[1]

    def main(self):
        clock = Clock()

        while True:
            clock.tick(60)
            self.update()
