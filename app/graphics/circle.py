import pygame
import pygame.gfxdraw


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

        pygame.gfxdraw.aacircle(*params)
        pygame.gfxdraw.filled_circle(*params)
