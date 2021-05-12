from pygame.time import Clock
from entity.player import PlayerEntity
from entity.bullet import BulletEntity


class Lobby:
    def __init__(self):
        self.entity_count = 0
        self.entities = {}
    
    def update(self):
        ids = set()
        for eid, entity in self.entities.items():
            if isinstance(entity, BulletEntity):
                if entity.is_out_of_bounds():
                    ids.add(eid)
                    continue
                for oid, other in self.entities.items():
                    if entity != other:
                        distance = entity.get_distance(other)
                        if distance != -1:
                            if distance < entity.radius+other.radius:
                                if isinstance(other, PlayerEntity):
                                    other.hp -= 1
                                    if other.hp > 0:
                                        ids.add(eid)
                                    if other.hp == 0:
                                        entity.entity.score += 1
                                        other.score -= 1
                                elif isinstance(other, BulletEntity):
                                    if oid not in ids:
                                        ids.add(eid)
                                        ids.add(oid)
            else:
                for oid, other in self.entities.items():
                    if entity != other:
                        distance = entity.get_distance(other)
                        if distance != -1:
                            if distance < entity.radius+other.radius:
                                if other.hp > 0 and entity.hp > 0:
                                    entity.hp = 0
                                    other.hp = 0
            entity.update()
        if ids:
            for eid in ids:
                self.entities.pop(eid)

    def main(self):
        clock = Clock()
        print('Lobby Running')

        while True:
            clock.tick(144)
            self.update()
