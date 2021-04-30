from player import ServerPlayer
from entity.player import PlayerEntity
from entity.bullet import BulletEntity


class EventHandler:
    def __init__(self, server):
        self.server = server
    
    def handle_events(self, events, player_id):
        if len(events) < 1:
            lobby_id = self.server.players[player_id].lobby_id
            if lobby_id == None:
                return self.server.lobbies
            return self.server.lobbies[lobby_id].entities

        for event, value in events.items():
            reply = self.handle_event(event, value, player_id)
        return reply
    
    def handle_event(self, event, value, player_id):
        lobby_id = self.server.players[player_id].lobby_id

        if lobby_id == None:
            if event == 'join':
                self.server.players[player_id].lobby_id = value[0]
                lobby = self.server.lobbies[value[0]]
                self.server.players[player_id].entity_id = lobby.entity_count
                lobby.entities[lobby.entity_count] = PlayerEntity(
                    value[1],
                    (150, 150, 150)
                )
                lobby.entity_count += 1
                return lobby.entity_count - 1
            return self.server.lobbies
        lobby = self.server.lobbies[lobby_id]
        player = lobby.entities[self.server.players[player_id].entity_id]
        if event == 'move':
            player.move = value
        elif event == 'shoot':
            lobby.entities[lobby.entity_count] = BulletEntity(player, value)
            lobby.entity_count += 1
        return lobby.entities
