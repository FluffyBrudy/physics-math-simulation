import numpy as np
import pygame
import pygame.gfxdraw as gfxdraw

from constants import DEFAULT_BORDER_RADIUS, DEFAULT_BORDER_WIDTH, FALLBACK_COLOR, HEIGHT, RED, WHITE, WIDTH


class SineWave:
    def __init__(self) -> None:
        w, h = WIDTH // 2, HEIGHT // 2

        self.surface = pygame.Surface((w, h), pygame.SRCALPHA)

        rect = pygame.Rect(0, 0, w - 10, h - 10)
        self.plot_points = self.prerenderWave(self.surface)
        self.pos = rect.midright

        self.slider = Slider((self.surface.width-10, rect.centery + rect.height + 10), 360, 40, (0, len(self.plot_points)) )

    def display(self, surface: pygame.Surface):
        surface.blit(self.surface, self.pos)
        self.slider.display(surface)

    def handle_event(self,event: pygame.Event):
        self.slider.update(event)

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

        return plot_points


class Slider:
    def __init__(self, pos: tuple[int, int], width: int, height: int, value_range: tuple[int, int], **kwargs):
        self.rect = pygame.Rect(*pos, width+height//4, int(height * 0.5))
        self.color = kwargs.get("color", FALLBACK_COLOR)
        self.border_width = kwargs.get("border_width", DEFAULT_BORDER_WIDTH)
        self.border_radius = kwargs.get("border_radius", DEFAULT_BORDER_RADIUS)

        pointer_size = height // 4
        self.slider_rect = pygame.Rect(pos, (pointer_size, pointer_size))
        self.slider_range = value_range
        self.lvalue = self.rect.left
        self.rvalue = self.rect.right-1

    def display(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.color, (self.slider_rect.centerx, self.rect.centery), self.slider_rect.height)
        pygame.draw.rect(surface, self.color, self.rect, self.border_width, self.border_radius)

    def update(self, event:pygame.Event):
        pos = event.pos
        if pygame.mouse.get_pressed()[0]:
            self.slider_rect.x = max(self.lvalue, min(pos[0],self.rvalue-self.slider_rect.height))

    def get_value(self):
        return self.slider_rect.x - self.lvalue