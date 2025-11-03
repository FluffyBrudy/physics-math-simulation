from typing import Dict, Tuple
import pygame
from pygame import Surface

TTilesType = Dict[Tuple[int, int], Surface]


class Tilemap:
    def __init__(self) -> None:
        self.tiles: TTilesType = {}

        wall_surf = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.rect(wall_surf, (100, 100, 100, 255), (0, 0, 32, 32))
        pygame.draw.rect(wall_surf, (50, 50, 50, 255), (0, 0, 32, 32), 2)

        for x in range(0, 12):
            self.tiles[(x, 0)] = wall_surf.copy()
            self.tiles[(x, 12)] = wall_surf.copy()

        for y in range(1, 12):
            self.tiles[(0, y)] = wall_surf.copy()
            self.tiles[(11, y)] = wall_surf.copy()

        for x in range(4, 8):
            for y in range(5, 7):
                self.tiles[(x, y)] = wall_surf.copy()

    def render(self, surface: Surface):
        for pos, tile in self.tiles.items():
            x, y = pos[0] * 32, pos[1] * 32
            surface.blit(tile, (x, y))
