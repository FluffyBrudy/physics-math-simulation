from typing import Optional
import numpy as np
import pygame
import pygame.gfxdraw as gfxdraw

from constants import DEFAULT_BORDER_RADIUS, DEFAULT_BORDER_WIDTH, FALLBACK_COLOR, HEIGHT, RED, WHITE, WIDTH


class SineWave:
    def __init__(self) -> None:
        w, h = WIDTH // 2, HEIGHT // 2

        self.staticsurf = pygame.Surface((w, h), pygame.SRCALPHA)
        self.surface = pygame.Surface((w, h), pygame.SRCALPHA)

        rect = pygame.Rect(0, 0, w - 10, h - 10)
        self.plot_points = self.prerenderWave(self.staticsurf)
        self.pos = rect.midright

        slider_width = len(self.plot_points)
        self.slider = Slider(
            pos=((WIDTH - slider_width) // 2 - 10, HEIGHT),
            width=slider_width, height=40, 
        )

    def display(self, surface: pygame.Surface):
        self.surface.fill((0, 0, 0, 0))
        self.surface.blit(self.staticsurf, (0, 0))

        wave_x, wave_y = self.plot_points[self.slider.get_value()]
        gfxdraw.filled_circle(self.surface, int(wave_x), int(wave_y), DEFAULT_BORDER_RADIUS, FALLBACK_COLOR)

        surface.blit(self.surface, self.pos)
        self.slider.display(surface)

    def update(self):
        self.slider.update()

    def get_current_angle(self):
        return self.slider.get_value()

    def get_container_pos(self):
        return self.pos

    @staticmethod
    def prerenderWave(surface: pygame.Surface):
        w, h = surface.get_size()
        x = np.linspace(0, 4 * np.pi, 721, endpoint=True)
        print(len(x))
        y = np.sin(x)

        pad_ratio = 0.85
        margin = (1 - pad_ratio) * w // 2

        padded_width = int(w * pad_ratio)
        padded_height = int(h * pad_ratio)

        x_pixels = margin + (x - x.min()) / (x.max() - x.min()) * padded_width
        y_pixels = margin + (1 - (y - y.min()) / (y.max() - y.min())) * padded_height

        plot_points = list(zip(x_pixels, y_pixels))
        gfxdraw.aapolygon(surface, plot_points, WHITE)
        pygame.draw.lines(surface, WHITE, False, plot_points, 2)

        return plot_points


class Slider:
    def __init__(self, pos: tuple[int, int], width: int, height: int, **kwargs):
        pointer_size = height // 3

        self.default_color = kwargs.get("color", FALLBACK_COLOR)
        self.hover_color = RED

        self.rect = pygame.Rect(*pos, width, int(height * 0.5))
        self.rect.bottom = pos[1] - (pointer_size // 2)
        self.color = self.default_color
        self.border_width = kwargs.get("border_width", DEFAULT_BORDER_WIDTH)
        self.border_radius = kwargs.get("border_radius", DEFAULT_BORDER_RADIUS)
        self.slider_rect = pygame.Rect(pos, (pointer_size, pointer_size))

        self.shallow_rect = self.rect.copy() # this is related with self.rect
        self.shallow_rect.width += self.slider_rect.width

        self.released = True

    def display(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.color, (self.slider_rect.centerx, self.rect.centery), self.slider_rect.height)
        pygame.draw.rect(surface, self.color, self.shallow_rect, self.border_width, self.border_radius)

    def update(self):
        pressed = pygame.mouse.get_pressed()[0]
        not_released_or_collided = (not self.released or self.rect.collidepoint(pygame.mouse.get_pos()))
        if pressed and not_released_or_collided:
            self.released = False
            pos = pygame.mouse.get_pos()
            self.slider_rect.x = max(self.rect.left, min(pos[0],self.rect.right-1))
        elif not pressed:
            self.released = True
        self.handle_state_indication(pressed and not_released_or_collided)

    def handle_state_indication(self, is_pressed: bool):
        if is_pressed:
            if self.color != self.hover_color:
                self.color = self.hover_color
        elif self.color != self.default_color:
            self.color = self.default_color

    def get_value(self):
        print(self.slider_rect.x-self.rect.left)
        return self.slider_rect.x - self.rect.left
