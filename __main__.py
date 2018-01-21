import pygame as pgm
from time import clock as clc
from physics.charge import Charge, tensity
from graphics.render import Render


if __name__ == '__main__':
    pgm.init()
    screen = pgm.display.set_mode((500, 500))
    charges_map = pgm.Surface((500, 500))
    charges_map.set_colorkey((0, 0, 0))
    field = pgm.Surface((500, 500))
    field.set_colorkey((0, 0, 0))
    tray = pgm.Surface((500, 20))
    tray.fill((50, 50, 50))
    trayfont = pgm.font.SysFont("monospace", 15)
    tray.blit(trayfont.render("Press 'r' to start rendering", 1, (255, 255, 0)), (5, 0))
    screen.blit(tray, (0, 480))
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
                screen.blit(tray, (0, 480))
                pgm.display.update()
            if e.type == pgm.KEYDOWN:
                if pgm.key.get_pressed()[pgm.K_r]:
                    field.fill((0, 0, 0))
                    myrender = Render(charges, charges_map, screen, field)
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
