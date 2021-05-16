class ServerPlayer:
    count = 0

    def __init__(self):
        ServerPlayer.count += 1
        self.lobby_id = None
        self.entity_id = None
