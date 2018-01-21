import pygame as pgm
from math import sin, cos
from time import clock as clc
from physics.charge import Charge, tensity
from graphics.render import trace
from graphics.tracer import Tracer
from physics.consts import *

if __name__ == '__main__':
    pgm.init()
    RES = (800, 700)
    screen = pgm.display.set_mode(RES)
    charges_map = pgm.Surface(RES)
    charges_map.set_colorkey((0, 0, 0))
    field = pgm.Surface(RES)
    field.set_colorkey((0, 0, 0))
    tray = pgm.Surface((RES[0], 20))
    tray.fill((50, 50, 50))
    trayfont = pgm.font.SysFont("monospace", 15)
    tray.blit(trayfont.render("Press 'r' to start rendering", 1, (255, 255, 0)), (7, 0))
    screen.blit(tray, (0, RES[1] - 20))
    pgm.display.update()
    rendering = False
    alive = True
    charges = []
    while alive:
        for e in pgm.event.get():
            if e.type == pgm.QUIT:
                alive = False
            if e.type == pgm.MOUSEBUTTONDOWN:
                if pgm.mouse.get_pressed()[0]:
                    charges.append(Charge(*pgm.mouse.get_pos(), value=1))
                elif pgm.mouse.get_pressed()[2]:
                    charges.append(Charge(*pgm.mouse.get_pos(), value=-1))
                charges[len(charges)-1].draw(charges_map)
                screen.fill((0, 0, 0))
                screen.blit(charges_map, (0, 0))
                screen.blit(tray, (0, 780))
                pgm.display.update()
            if e.type == pgm.KEYDOWN:
                if pgm.key.get_pressed()[pgm.K_r]:
                    field.fill((0, 0, 0))
                    launches = []
                    fi = 0
                    while fi < twopi:
                        for q in charges:
                            if q.value == 1:
                                launches.append([q.x - (QRAD+1) * cos(fi), q.y - (QRAD+1) * sin(fi)])
                        fi += ANG_INCR
                    workers = [Tracer(trace, (charges, charges_map, screen, field)) for i in range(WORKERS_COUNT)]
                    for i in range(len(launches)):
                        workers[i % WORKERS_COUNT].put(launches[i])
                    for w in workers:
                        w.start()
                    rendering = True
                    t_start = clc()
            """
                screen.fill((0, 0, 0))
                screen.blit(field, (0, 0))
                screen.blit(charges_map, (0, 0))
                tray.fill((50, 50, 50))
                tray.blit(trayfont.render("Rendering: {:0.1f}%".format(myrender.proc),
                                          1, (255, 255, 0)), (5, 0))
                screen.blit(tray, (0, 480))
                pgm.display.update()
            else:
                tray.fill((50, 50, 50))
                tray.blit(trayfont.render("Finished (in ~{:0.1f}s)".format(clc()-t_start),
                                          1, (255, 255, 0)), (5, 0))
                screen.blit(tray, (0, 480))
                pgm.display.update()
                rendering = False
            """
    pgm.quit()
