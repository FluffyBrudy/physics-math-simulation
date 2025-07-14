import math
from random import randint
from typing import Optional
import pygame
from circle import Particle
from constants import BLACK, CIRCLE_SIZE_RANGE, SCREENHEIGHT, SCREENSIZE, SCREENWIDTH, WHITE


class Physic:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Physics Simulation")
        self.displaySurf = pygame.display.set_mode((SCREENSIZE))
        self.clock = pygame.time.Clock()

        self.running = True

        self.particles: list[Particle] = []
        self.spawnParticles(2)

        self.selectedParticle: Optional[Particle] = None

    def spawnParticles(self, n: int):
        for _ in range(n):
            size = randint(*CIRCLE_SIZE_RANGE)
            x  = randint(size, SCREENWIDTH - size)
            y  = randint(size, SCREENHEIGHT - size)
            particle = Particle(x, y, size)
            self.particles.append(particle)

    def findParticle(self, pos: tuple[int, int]):
        if self.selectedParticle:
            return self.selectedParticle
        for particle in self.particles:
            posX = particle.x - pos[0]
            posY = particle.y - pos[1]
            if math.hypot(posX, posY) <= particle.size:
                return particle
        return None

    def draw(self):
        self.displaySurf.fill(BLACK)
        for i, particle in enumerate(self.particles):
            if self.selectedParticle != particle:
                particle.move()
                particle.bounce()
                for otherParticle in self.particles[i+1:]:
                    self.handleCollision(particle, otherParticle)
            particle.display(self.displaySurf)

    def handleCollision(self, p1: Particle, p2: Particle):
        dx = p1.x - p2.x
        dy = p1.y - p2.y

        distance = math.hypot(dx, dy)
        if distance < (p1.size + p2.size):
            tangent = math.atan()

    def handleEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.selectedParticle = self.findParticle(event.pos)
                if self.selectedParticle:
                    self.selectedParticle.set_at(event.pos)
            if self.selectedParticle and event.type == pygame.MOUSEMOTION:
                mouseX, mouseY = event.pos
                dx = mouseX - self.selectedParticle.x
                dy = mouseY - self.selectedParticle.y
                self.selectedParticle.set_at(Particle.clipAround((mouseX, mouseY), self.selectedParticle))
                self.selectedParticle.speed = math.hypot(dx, dy) * 0.1
                self.selectedParticle.angle = math.atan2(dy, dx)
            if event.type == pygame.MOUSEBUTTONUP:
                if self.selectedParticle:
                    self.selectedParticle = None

    def run(self):
        while self.running:
            self.handleEvent()
            self.draw()
            pygame.display.flip()
        pygame.quit()


def main():
    physics = Physic()
    physics.run(
)

if __name__ == "__main__":
    main()
