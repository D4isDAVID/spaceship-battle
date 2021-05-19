from entity.player import PlayerEntity
from entity.bullet import BulletEntity


class Lobby:
    TARGET_FPS = 144

    def __init__(self):
        self.players = []
        self.entity_count = 0
        self.entities = {}
    
    def update(self, delta_time):
        ids = set()
        for eid in list(self.entities.keys()):
            try:
                entity = self.entities[eid]
            except Exception:
                pass
            else:
                if isinstance(entity, BulletEntity):
                    if entity.is_out_of_bounds():
                        ids.add(eid)
                    if entity.get_distance(entity.original_shooter) > 1600:
                        ids.add(eid)
                    for oid in list(self.entities.keys()):
                        try:
                            other = self.entities[oid]
                        except Exception:
                            pass
                        else:
                            if entity != other:
                                distance = entity.get_distance(other)
                                if distance != -1:
                                    if entity.shooter != other:
                                        if isinstance(other, PlayerEntity):
                                            if distance < entity.RADIUS+other.RADIUS:
                                                other.hp -= 1
                                                if other.hp >= 0:
                                                    ids.add(eid)
                                                if other.hp == 0:
                                                    entity.shooter.score += 1
                                        elif isinstance(other, BulletEntity):
                                            if distance < entity.RADIUS+other.RADIUS:
                                                if oid not in ids:
                                                    ids.add(eid)
                                                    ids.add(oid)
                else:
                    for oid in list(self.entities.keys()):
                        try:
                            other = self.entities[oid]
                        except Exception:
                            pass
                        else:
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
