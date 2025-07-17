from math import sin, cos, radians
from pygame import Surface, gfxdraw
import pygame
from constants import DEFAULT_BORDER_WIDTH, SKYBLUE_COLOR


class Circle:
    def __init__(self, center: tuple[int, int], radius: int, init_angle: float) -> None:
        self.angle = init_angle
        self.center = center
        self.radius = radius
        self.font = pygame.font.Font(None, 24)

    def display(self, surface: Surface):
        end_pos_x = self.center[0] + int(round(self.radius * cos(radians(self.angle))))
        end_pos_y = self.center[1] + int(round(self.radius * sin(radians(self.angle))))
        end_pos = (end_pos_x, end_pos_y)

        pygame.draw.circle(surface, SKYBLUE_COLOR, self.center, self.radius, DEFAULT_BORDER_WIDTH)
        gfxdraw.aacircle(surface, self.center[0], self.center[1], self.radius, SKYBLUE_COLOR)
        pygame.draw.line(surface, SKYBLUE_COLOR, self.center, end_pos, DEFAULT_BORDER_WIDTH)

        pygame.draw.line(surface, SKYBLUE_COLOR, end_pos, (end_pos[0], self.center[1]), DEFAULT_BORDER_WIDTH)
        pygame.draw.line(surface, SKYBLUE_COLOR, (self.center[0]-self.radius, self.center[1]), (self.center[0]+self.radius, self.center[1]), DEFAULT_BORDER_WIDTH)
        pygame.draw.line(surface, SKYBLUE_COLOR, (self.center[0], self.center[1]-self.radius), (self.center[0], self.center[1]+self.radius), DEFAULT_BORDER_WIDTH)

        self.render_angle(surface)

    def update_angle(self, angle: float):
        self.angle = angle

    def render_angle(self, surface: Surface):
        angle_text = f"{self.angle:.1f}°"
        text_surface = self.font.render(angle_text, True, SKYBLUE_COLOR)
        text_x = self.center[0] + int(round((self.radius + text_surface.width) * cos(radians(self.angle))))
        text_y = self.center[1] + int(round((self.radius + text_surface.width) * sin(radians(self.angle))))
        text_rect = text_surface.get_rect(center=(text_x, text_y))
        surface.blit(text_surface, text_rect)