from request_client import Client
import pygame
import math


class Lobby:
    def __init__(self):
        self.entities = []
        self.entity_id = None
        self.move = [False, False, False, False, False]
    
    def draw(self, surface):
        surface.fill(0)
        for entity in list(self.entities.values()):
            entity.draw(surface)

    def main(self, name, hostname, port=7723):
        window = pygame.display.set_mode((1280, 720))
        client = Client(hostname, port)
        self.entity_id = client.send({'join': [0, name]})
        self.entities = client.send({})

        while True:
            self.draw(window)
            pygame.display.update()

            events = {}
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w: self.move[0] = True
                    elif event.key == pygame.K_a: self.move[1] = True
                    elif event.key == pygame.K_s: self.move[2] = True
                    elif event.key == pygame.K_d: self.move[3] = True
                    elif event.key == pygame.K_LSHIFT: self.move[4] = True
                    events['move'] = self.move
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:self.move[0] = False
                    elif event.key == pygame.K_a: self.move[1] = False
                    elif event.key == pygame.K_s: self.move[2] = False
                    elif event.key == pygame.K_d: self.move[3] = False
                    elif event.key == pygame.K_LSHIFT: self.move[4] = False
                    events['move'] = self.move
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    pos = [
                        pos[0]-self.entities[self.entity_id].x,
                        pos[1]-self.entities[self.entity_id].y
                    ]

                    events['shoot'] = math.atan2(pos[1], pos[0]) / math.pi * 180

            self.entities = client.send(events)


if __name__ == '__main__':
    lobby = Lobby()
    ip = input("Ented Server IP: ")
    name = input("Enter Desired Name: ")
    lobby.main(name, ip, 7723)
