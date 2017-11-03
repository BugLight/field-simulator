import pygame as pgm
# from pygame import *

if __name__ == '__main__':
    pgm.init()
    screen = pgm.display.set_mode((500, 500))
    alive = True
    while alive:
        for e in pgm.event.get():
            if e.type == pgm.QUIT:
                alive = False
        pgm.display.update()
    pgm.quit()
