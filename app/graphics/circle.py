import pygame
from pygame import gfxdraw


class Circle:
    def __init__(self, point, radius, color):
        self.point = point
        self.radius = radius
        self.color = color

    def draw(self, surface):
        params = (
            surface,
            *tuple(map(int, self.point)),
            self.radius,
            self.color
        )

        gfxdraw.aacircle(*params)
        gfxdraw.filled_circle(*params)
