import math
from typing import Literal, Union
from pygame import Event, Surface
from random import random, uniform
from pygame.event import EventType
import pygame.gfxdraw as gfxdraw
from constants import BLACK, CIRCLE_THICKNESS, DRAG, ELASTICITY, GRAVITY, RED, SCREENHEIGHT, SCREENWIDTH, WHITE


class Particle:
    def __init__(self, x: int, y: int, size: int):
        self.x = x
        self.y = y
        self.size = size
        self.color: tuple[int, int, int] = RED

        self.speed = random()
        self.angle = uniform(0, math.pi / 2)


    def display(self, surface: Surface):
        x, y = int(self.x), int(self.y)
        gfxdraw.aacircle(surface, x, y, self.size, self.color)
        # gfxdraw.filled_circle(surface, x, y, self.size - CIRCLE_THICKNESS, self.color)

    def move(self):
        self.angle, self.speed = Particle.addVectors((self.angle, self.speed), GRAVITY)
        self.x += math.cos(self.angle) * self.speed
        self.y -= math.sin(self.angle) * self.speed
        self.speed *= DRAG

    def bounce(self):
        hasBounce = self.x < self.size or self.x > SCREENWIDTH - self.size or \
                    self.y < self.size or self.y >= SCREENHEIGHT - self.size
        if self.x < self.size: 
            self.angle = math.pi-self.angle
            self.x = self.size
        elif self.x > SCREENWIDTH - self.size:
            self.angle = math.pi - self.angle
            self.x = (SCREENWIDTH - self.size)
        if self.y < self.size:
            self.angle = -self.angle
            self.y = self.size
        elif self.y >= SCREENHEIGHT - self.size:
            self.angle = -self.angle
            self.y =(SCREENHEIGHT - self.size)
        if hasBounce:
            self.speed *= ELASTICITY

    def set_at(self, pos: tuple[int, int]):
        self.x = pos[0]
        self.y = pos[1]

    @staticmethod
    def addVectors(polar1: tuple[float, float], polar2: tuple[float, float]):
        """
            Args:
                takes two polar points where first element is angle second is length
                polar1: Tuple[float, float]
                polar2: Tuple[float, float]
            Returns: Tuple[float, float] 
                angle: float
                length: float
        """
        angle1, angle2 = polar1[0], polar2[0]
        len1, len2 = polar1[1], polar2[1]
        x = math.cos(angle1) * len1 + math.cos(angle2) * len2
        y = math.sin(angle1) * len1 + math.sin(angle2) * len2
        length = math.hypot(x, y)
        angle =  math.atan2(y,x)
        return angle, length

    @staticmethod
    def clipAround(pos: tuple[int, int], particle: 'Particle'):
        return (
            max(particle.size, min(pos[0], SCREENWIDTH - particle.size)),
            max(particle.size, min(pos[1], SCREENHEIGHT - particle.size))
        )