from entity.player import PlayerEntity
from entity.bullet import BulletEntity


class Lobby:
    count = 0
    TARGET_FPS = 144
    MAX_PLAYERS = 6

    def __init__(self):
        Lobby.count += 1
        self.players = 0
        self.entity_count = 0
        self.entities = {}
    
    def update(self, delta_time):
        ids = set()
        for entity_id in list(self.entities.keys()):
            if entity_id in self.entities:
                entity = self.entities[entity_id]
                if isinstance(entity, BulletEntity):
                    if entity.is_out_of_bounds():
                        ids.add(entity_id)
                    if entity.get_distance(entity.original_shooter) > 1600:
                        ids.add(entity_id)
                    for other_id in list(self.entities.keys()):
                        if other_id in self.entities:
                            other = self.entities[other_id]
                            if entity != other:
                                distance = entity.get_distance(other)
                                if distance != -1:
                                    if entity.shooter != other:
                                        if isinstance(other, PlayerEntity):
                                            if distance < entity.RADIUS+other.RADIUS:
                                                other.hp -= 1
                                                if other.hp >= 0:
                                                    ids.add(entity_id)
                                                if other.hp == 0:
                                                    entity.shooter.score += 1
                                        elif isinstance(other, BulletEntity):
                                            if distance < entity.RADIUS+other.RADIUS:
                                                if other_id not in ids:
                                                    ids.add(entity_id)
                                                    ids.add(other_id)
                else:
                    for other_id in list(self.entities.keys()):
                        if other_id in self.entities:
                            other = self.entities[other_id]
                            if entity != other:
                                distance = entity.get_distance(other)
                                if distance != -1:
                                    if distance < entity.RADIUS+other.RADIUS:
                                        if other.hp > 0 and entity.hp > 0:
                                            entity.hp = 0
                                            other.hp = 0
                entity.update(delta_time, self.TARGET_FPS)
        if ids:
            for eid in ids:
                self.entities.pop(eid)
    
    def serialize(self):
        serialized = ''
        
        for entity_id in list(self.entities.keys()):
            try:
                entity = self.entities[entity_id]
            except KeyError:
                pass
            else:
                if serialized != '': serialized += '|'
                serialized += f'{entity_id}-{entity.x},{entity.y}'
                if isinstance(entity, PlayerEntity):
                    serialized += f',{entity.rotation},{entity.score},{entity.hp},{entity.move_time}'
                    for i in entity.move:
                        serialized += f',{int(i)}'
                    serialized += f',{entity.name}'
                elif isinstance(entity, BulletEntity):
                    serialized += f',{entity.shooter_id}'
                    for i in entity.velocity:
                        serialized += f',{i}'
        serialized += '||'
        return serialized
