from typing import Dict, Literal, TYPE_CHECKING, Optional, Tuple
from pygame import Rect, Surface
import pygame
from pygame.typing import Point


if TYPE_CHECKING:
    from main import Game
    from tilemap import TTilesType


TCollisionTypeKeys = Literal["left", "right", "up", "down"]
TCollisionType = Dict[TCollisionTypeKeys, bool]
TCollisionProbeType = Dict[TCollisionTypeKeys, Tuple[int, int]]

CONTACT_TOLERANCE = 2


class Player:
    def __init__(self, game: "Game", pos: Point) -> None:
        self.game = game

        self.image = pygame.Surface((16, 32))
        self.image.fill("red")

        self.pos = pygame.math.Vector2(pos)
        self.velocity = pygame.Vector2((0, 0))
        self.speed = 200
        self.dashing = 0
        self.flipped = False

        self.prev_movement_x = 0

        self.collisions: TCollisionType = {
            "left": False,
            "right": False,
            "up": False,
            "down": False,
        }
        self.collision_probe: TCollisionProbeType = {
            "left": (-1, 0),
            "right": (1, 0),
            "up": (0, -1),
            "down": (0, 1),
        }

        self.font = pygame.font.SysFont(None, 25)

    def rect(self):
        return Rect(self.pos, self.image.size).inflate(-10, -10)

    def handle_flip(self, movement: Point):
        if movement[0] and movement[0] != self.prev_movement_x:
            self.prev_movement_x = movement[0]
        if movement[0] < 0:
            self.flipped = True
        elif movement[0] > 0:
            self.flipped = False

    def apply_gravity(self):
        self.velocity.y = round(min(self.velocity.y + 0.1, 10), 2)

    def tile_collision_x(self, xdir: float):
        player_rect = self.rect()
        collided: Optional[Literal["left", "right"]] = None

        for tx, ty in self.game.tilemap.tiles:
            x, y = tx * 32, ty * 32
            tile_rect = Rect(x, y, 32, 32)
            delta = 0
            if player_rect.colliderect(tile_rect):
                if xdir < 0:
                    collided = "left"
                    delta = tile_rect.right - player_rect.left
                    self.collisions["left"] = True
                elif xdir > 0:
                    collided = "right"
                    delta = tile_rect.left - player_rect.right
                    self.collisions["right"] = True
                self.pos.x += delta
                break

        self.probe_collision(self.game.tilemap.tiles, "left", "right")

        return collided is not None

    def tile_collision_y(self, ydir: float):
        player_rect = self.rect()
        collided: Optional[Literal["up", "down"]] = None

        for tx, ty in self.game.tilemap.tiles:
            tile_rect = Rect(tx * 32, ty * 32, 32, 32)
            delta = 0
            if player_rect.colliderect(tile_rect):
                if ydir < 0:
                    collided = "up"
                    delta = tile_rect.bottom - player_rect.top
                    self.collisions["up"] = True
                elif ydir > 0:
                    collided = "down"
                    self.collisions["down"] = True
                    delta = tile_rect.top - player_rect.bottom
                self.pos.y += delta
                break

        self.probe_collision(self.game.tilemap.tiles, "down")

        return collided is not None

    def probe_collision(self, tiles: "TTilesType", *sides: TCollisionTypeKeys):
        for tile in tiles:
            for side in sides:
                probe_offset = self.collision_probe[side]
                tile_pos = tile[0] * 32, tile[1] * 32
                if self.rect().move(probe_offset).colliderect(tile_pos, (32, 32)):
                    self.collisions[side] = True
                    break

    def jump(self):
        self.velocity.y = -3

    def dash(self):
        side_colliding = self.collisions["left"] or self.collisions["right"]
        if not self.dashing and not side_colliding:
            self.dashing = 10

    def handle_dash(self):
        if self.dashing:
            if abs(self.dashing) < 5:
                self.dashing = 0
                self.velocity.x = 0
            elif abs(self.dashing) >= 5:
                flip_dir = -1 if self.flipped else 1
                self.velocity.x = flip_dir * 10
                self.dashing -= 1

    def apply_friction(self):
        if self.velocity.x < 0:
            self.velocity.x = min(0, self.velocity.x + 1)
        elif self.velocity.x > 0:
            self.velocity.x = max(0, self.velocity.x - 1)

        if self.collisions["left"] or self.collisions["right"]:
            self.dashing = 0
            self.velocity.x = 0

    def update(self, dt: float, movement=(0, 0)):
        self.collisions = {"left": False, "right": False, "up": False, "down": False}

        movement_x = self.speed * dt * (self.velocity.x + movement[0])
        movement_y = self.speed * dt * (self.velocity.y + movement[1])

        self.pos.x += movement_x
        if self.tile_collision_x(movement_x):
            self.velocity.x = 0

        self.pos.y += movement_y
        if self.tile_collision_y(movement_y):
            self.velocity.y = 0

        self.apply_gravity()
        self.handle_flip(movement)
        self.handle_dash()
        self.apply_friction()

    def render(self, surface: Surface):
        text = self.font.render(
            f"{self.dashing}",
            True,
            (255, 255, 255),
        )
        surface.blit(self.image, self.pos)
        surface.blit(text, (0, 600))
