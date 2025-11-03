from typing import Dict, Tuple

from pygame import Surface
import pygame


TTilesType = Dict[Tuple[int, int], Surface]


class Tilemap:
    def __init__(self) -> None:
        surf = pygame.Surface((32, 32), pygame.SRCALPHA)
        self.tiles: TTilesType = {(x, 10): surf for x in range(0, 12)}

    def render(self, surface: Surface):
        for pos, tile in self.tiles.items():
            x, y = pos[0] * 32, pos[1] * 32
            pygame.draw.rect(tile, (0, 250, 0, 150), (0, 0, 32, 32))
            pygame.draw.rect(tile, (0, 250, 0, 255), (0, 0, 32, 32), 2)
            surface.blit(tile, (x, y))
