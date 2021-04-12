import pygame
from network import Network
from controller import Controller


class Game:
    WIDTH, HEIGHT = 1280, 720

    def __init__(self):
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.name = ''
        self.players = {}
    
    def draw(self):
        self.window.fill(0)
        for player in self.players:
            player.draw(self.window)
    
    def main(self):
        running = True
        clock = pygame.time.Clock()
        client = Network(input("Enter Server IP: "))
        self.name = client.auth(input("Enter Desired Name: "))
        controller = Controller(client)

        while running:
            clock.tick(60)

            controller.move()
            self.players = client.get()

            self.draw()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.main()
