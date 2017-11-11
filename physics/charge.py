from . import Vector2D
import pygame as pgm
from math import sqrt, sin, cos, pi
from .consts import APPR_TOL_SQ, MAX_FAR_SQ, QRAD, PCOL, NCOL, GREY, twopi

class Charge(Vector2D):
    def __init__(self, x, y, value):
        Vector2D.__init__(self, x, y)
        self.value = value

    def draw(self, surface):
        color = PCOL if self.value > 0 else NCOL
        pgm.draw.circle(surface, color, (self.x, self.y), QRAD, 0)

    def tensity(self, x, y):
        v = Vector2D(x, y) - self
        length = v.length()
        if length:
            return v*(self.value/length**3)
        return Vector2D(0, 0)


def tensity(charges, x, y):
    v = Vector2D(0, 0)
    for c in charges:
        v += c.tensity(x, y)
    return v
