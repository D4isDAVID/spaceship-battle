import pygame
from network import Network
from controller import Controller
from time import sleep


class Game:
    WIDTH, HEIGHT = 1280, 720

    def __init__(self):
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.name = ''
        self.players = {}
    
    def draw(self):
        self.window.fill(0)
        for player in self.players:
            if player.name == self.name:
                player.drawentity(self.window)
                point = (player.x+player.width//2, player.y-20)
                size = 7
                arrow = (point,
                         (point[0]-size*(2), point[1]-size*2),
                         (point[0], point[1]-round(size*2/3)),
                         (point[0]+size*2, point[1]-size*2))
                pygame.draw.polygon(self.window, player.color, arrow)
            else:
                player.draw(self.window)
    
    def main(self):
        running = True
        clock = pygame.time.Clock()
        client = Network(input("Enter Server IP: "))
        while client.id == None:
            client = Network(input("Enter Server IP: "))
        self.name = client.auth(input("Enter Desired Name: "))
        controller = Controller(client)

        while running:
            clock.tick(60)

            move_data = controller.move()
            if move_data == '':
                self.players = client.get()
            else:
                self.players = client.post(move_data)

            self.draw()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.main()
