from typing import Dict, Literal
from pygame import Surface
import pygame
from pygame.typing import Point


TCollisionType = Dict[Literal["left", "right", "up", "down"], bool]


class Player:
    def __init__(self, pos: Point) -> None:
        self.image = pygame.Surface((16, 32))
        self.image.fill("red")

        self.pos = pygame.math.Vector2(pos)
        self.velocity = pygame.Vector2((0, 0))
        self.speed = 200

        self.prev_movement_x = 0

        self.collisions: TCollisionType = {
            "left": False,
            "right": False,
            "up": False,
            "down": False,
        }

    def rect(self):
        return pygame.Rect(*self.pos, *self.image.size)  # type: ignore

    def handle_movement(self, dt: float, movement: Point):
        movement_x = dt * (self.velocity.x + self.speed) * movement[0]
        movement_y = dt * (self.velocity.y + self.speed * 0.5)

        self.pos += (movement_x, movement_y)

        if movement[0] and movement[0] != self.prev_movement_x:
            self.prev_movement_x = movement[0]

    def tile_collision(self):
        pass

    def jump(self):
        self.velocity.y = -3

    def update(self, dt: float, movement=(0, 0)):
        self.handle_movement(dt, movement)

    def render(self, surface: Surface):
        surface.blit(self.image, self.pos)
