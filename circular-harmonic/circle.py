

from math import sin, cos, radians
from pygame import Surface, gfxdraw
import pygame
from constants import DEFAULT_BORDER_WIDTH, SKYBLUE_COLOR


class Circle:
    def __init__(self, center: tuple[int, int], radius: int, init_angle: float) -> None:
        self.angle = init_angle
        self.center = center
        self.radius = radius
        print(self.angle)

    def display(self, surface: Surface):
        pygame.draw.circle(surface, SKYBLUE_COLOR, self.center, self.radius, DEFAULT_BORDER_WIDTH)
        gfxdraw.aacircle(surface, self.center[0], self.center[1], self.radius, SKYBLUE_COLOR)
        end_pos_x = self.center[0] + int(round(self.radius * cos(radians(self.angle))))
        end_pos_y = self.center[1] + int(round(self.radius * sin(radians(self.angle))))
        end_pos = (end_pos_x, end_pos_y)
        pygame.draw.line(surface, SKYBLUE_COLOR, self.center, end_pos, DEFAULT_BORDER_WIDTH)

    def update_angle(self, angle: float):
        self.angle = angle