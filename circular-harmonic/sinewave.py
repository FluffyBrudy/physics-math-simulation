import numpy as np
import pygame
import pygame.gfxdraw as gfxdraw

from constatnts import HEIGHT, WHITE, WIDTH


class SineWave:
    def __init__(self, pos: tuple[int, int]) -> None:
        w, h = WIDTH // 2, HEIGHT // 2

        pad_ratio = 0.85

        padded_width = int(w * pad_ratio)
        padded_height = int(h * pad_ratio)

        "we are going 2 cycle for better example"
        x = np.linspace(0, 4 * np.pi, 500)
        y = np.sin(x)

        x_pixels = (x - x.min()) / (x.max() - x.min()) * padded_width
        y_pixels = (1 - (y - y.min()) / (y.max() - y.min())) * padded_height

        self.plot_points = list(zip(x_pixels, y_pixels))

        self.surface = pygame.Surface((w, h), pygame.SRCALPHA)
        self.prerenderWave(self.surface)
        self.pos = pygame.Rect(0, 0, w - 10, h - 10).midright

    def display(self, surface: pygame.Surface):
        surface.blit(self.surface, self.pos)

    def draw_cursor(self):
        pass

    @staticmethod
    def prerenderWave(surface: pygame.Surface):
        w, h = surface.get_size()
        x = np.linspace(0, 4 * np.pi, 500)  
        y = np.sin(x)

        pad_ratio = 0.85

        padded_width = int(w * pad_ratio)
        padded_height = int(h * pad_ratio)

        x_pixels = (x - x.min()) / (x.max() - x.min()) * padded_width
        y_pixels = (1 - (y - y.min()) / (y.max() - y.min())) * padded_height

        plot_points = list(zip(x_pixels, y_pixels))
        gfxdraw.aapolygon(surface, plot_points, WHITE)
        pygame.draw.lines(surface, WHITE, False, plot_points, 2)
