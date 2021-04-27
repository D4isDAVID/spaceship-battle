from player import ServerPlayer
from lobby_objects.entity.player import PlayerEntity


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
                lobby.entities.append(PlayerEntity(
                    value[1],
                    (255, 255, 255),
                    player_id
                ))
                return lobby.players[player_id].entity_id
            return self.server.lobbies
        lobby = self.server.lobbies[lobby_id]
        player = lobby.players[player_id]
        if event == 'move':
            lobby.entities[player.entity_id].move = value
        elif event == 'look':
            player.angle = value
        return lobby.entities
