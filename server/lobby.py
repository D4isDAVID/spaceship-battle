from pygame.time import Clock
from entity.player import PlayerEntity
from entity.bullet import BulletEntity


class Lobby:
    PLAYER_MAX = 16
    MAX_PLAYERS = 8

    def __init__(self):
        self.entity_count = 0
        self.entities = {}
    
    def update(self):
        ids = []
        for eid, entity in self.entities.items():
            entity.update()
            if entity.is_out_of_bounds():
                if isinstance(entity, BulletEntity):
                    ids.append(eid)
        if len(ids) > 0:
            for eid in ids:
                self.entities.pop(eid)

    def main(self):
        clock = Clock()
        print('Lobby Running')

        while True:
            clock.tick(60)
            self.update()
