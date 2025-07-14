import pygame
import sys
import constatnts as c
from sinewave import SineWave


pygame.init()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((c.WIDTH, c.HEIGHT))
        pygame.display.set_caption("trigonometic-wave-circle relation")
        self.clock = pygame.time.Clock()
        self.running = True

        self.waveSurf = SineWave((100, c.HEIGHT//2))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        pass

    def draw(self):
        self.screen.fill(c.BLACK)
        self.waveSurf.display(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(c.FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()
