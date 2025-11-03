from typing import Dict, Literal, TYPE_CHECKING
from pygame import Rect, Surface
import pygame
from pygame.typing import Point

if TYPE_CHECKING:
    from main import Game


TCollisionType = Dict[Literal["left", "right", "up", "down"], bool]


class Player:
    def __init__(self, game: "Game", pos: Point) -> None:
        self.game = game

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

    def update_movement(self, movement: Point):
        if movement[0] and movement[0] != self.prev_movement_x:
            self.prev_movement_x = movement[0]

    def apply_gravity(self):
        self.velocity.y = min(self.velocity.y + 0.1, 10)
        print(self.velocity.y)

    def tile_collision_x(self, xdir: float):
        player_rect = self.rect()
        for tx, ty in self.game.tilemap.tiles:
            x, y = tx * 32, ty * 32
            tile_rect = Rect(x, y, 32, 32)
            if player_rect.colliderect(tile_rect):
                if xdir < 0:
                    player_rect.left = tile_rect.right
                    self.collisions["left"] = True
                elif xdir > 0:
                    player_rect.right = tile_rect.left
                    self.collisions["right"] = True
                self.pos.x = player_rect.x
                return True
        return False

    def tile_collision_y(self, ydir: float):
        player_rect = self.rect()
        for tx, ty in self.game.tilemap.tiles:
            x, y = tx * 32, ty * 32
            tile_rect = Rect(x, y, 32, 32)
            if player_rect.colliderect(tile_rect):
                if ydir < 0:
                    self.collisions["up"] = True
                    player_rect.top = tile_rect.bottom
                elif ydir > 0:
                    self.collisions["down"] = True
                    player_rect.bottom = tile_rect.top
                self.pos.y = player_rect.y
                return True
        return False

    def jump(self):
        self.velocity.y = -3

    def update(self, dt: float, movement=(0, 0)):
        self.collisions = {"left": False, "right": False, "up": False, "down": False}

        self.apply_gravity()
        self.update_movement(movement)

        movement_x = self.speed * dt * (self.velocity.x + movement[0])
        movement_y = self.speed * dt * (self.velocity.y + movement[1])

        self.pos.x += movement_x
        if self.tile_collision_x(movement_x):
            self.velocity.x = 0

        self.pos.y += movement_y
        if self.tile_collision_y(movement_y):
            self.velocity.y = 0

    def render(self, surface: Surface):
        surface.blit(self.image, self.pos)
