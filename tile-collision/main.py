import pygame
import sys

from player import Player
from tilemap import Tilemap


class Game:
    def __init__(self, width=1280, height=720, title="Game"):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0

        self.player = Player(self, (100, 150))
        self.movement_x = [False, False]  # [left, right]

        self.tilemap = Tilemap()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.movement_x[0] = True
                elif event.key == pygame.K_RIGHT:
                    self.movement_x[1] = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.movement_x[0] = False
                elif event.key == pygame.K_RIGHT:
                    self.movement_x[1] = False
                if event.key == pygame.K_UP:
                    self.player.jump()
                if event.key == pygame.K_SPACE:
                    print(0)
                    self.player.dash()

    def update(self, dt):
        movement_x = (self.movement_x[1] - self.movement_x[0], 0)
        self.player.update(dt, movement_x)

    def render(self):
        self.screen.fill((0, 0, 0))
        self.tilemap.render(self.screen)
        self.player.render(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.dt = self.clock.tick(60) / 1000.0

            self.handle_events()
            self.update(self.dt)
            self.render()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
