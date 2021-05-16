import pygame
from entity.player import PlayerEntity
from entity.bullet import BulletEntity


class Lobby:
    TARGET_FPS = 144

    def __init__(self):
        self.entity_count = 0
        self.entities = {}
    
    def update(self, delta_time):
        ids = set()
        for eid in list(self.entities.keys()):
            entity = self.entities[eid]
            if isinstance(entity, BulletEntity):
                if entity.is_out_of_bounds():
                    ids.add(eid)
                if entity.get_distance(entity.original_entity) > 1600:
                    ids.add(eid)
                for oid in list(self.entities.keys()):
                    other = self.entities[oid]
                    if entity != other:
                        distance = entity.get_distance(other)
                        if distance != -1:
                            if entity.entity != other:
                                if isinstance(other, PlayerEntity):
                                    if distance < entity.radius+other.radius:
                                        other.hp -= 1
                                        if other.hp >= 0:
                                            ids.add(eid)
                                        if other.hp == 0:
                                            entity.entity.score += 1
                                elif isinstance(other, BulletEntity):
                                    if distance < entity.radius+other.radius:
                                        if oid not in ids:
                                            ids.add(eid)
                                            ids.add(oid)
            else:
                for oid in list(self.entities.keys()):
                    other = self.entities[oid]
                    if entity != other:
                        distance = entity.get_distance(other)
                        if distance != -1:
                            if distance < entity.radius+other.radius:
                                if other.hp > 0 and entity.hp > 0:
                                    entity.hp = 0
                                    other.hp = 0
            entity.update(delta_time, self.TARGET_FPS)
        if ids:
            for eid in ids:
                self.entities.pop(eid)

    def main(self):
        clock = pygame.time.Clock()
        print('Lobby Running')

        while True:
            delta_time = clock.tick(0) / 1000
            self.update(delta_time)
