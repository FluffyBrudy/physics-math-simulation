import pygame
import sys
from circle import Circle
import constants as c
from sinewave import SineWave

pygame.init()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((c.WIDTH, c.HEIGHT))
        pygame.display.set_caption("trigonometic-wave-circle relation")
        self.clock = pygame.time.Clock()
        self.running = True

        self.waveSurf = SineWave()
        circle_x = (c.WIDTH - self.waveSurf.get_container_pos()[0]) // 2
        self.circle = Circle((circle_x, c.HEIGHT // 2), int(c.WIDTH // 6), self.waveSurf.get_current_angle())

    def update(self):
        self.waveSurf.update()
        self.circle.update_angle(self.waveSurf.get_current_angle())

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def draw(self):
        self.screen.fill(c.BLACK)
        self.waveSurf.display(self.screen)
        self.circle.display(self.screen)
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
