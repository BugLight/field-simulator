import sys
sys.path.append('..')
from physics import Vector2D
import pygame as pgm
from math import sin, cos
from physics.charge import Charge, tensity
from physics.consts import *
from .tracer import Tracer

def trace(launch, charges, ch_map, screen, surface):
    def check_appr():
        nonlocal round_pos
        round_pos = [round(cur_pos[0]), round(cur_pos[1])]
        if (0 <= round_pos[0] < frame[0] and
            0 <= round_pos[1] < frame[1]):
            inside = True
            color = ch_map.get_at(round_pos)
            if color == PCOL or color == NCOL:
                return False
        else:
            inside = False
        if force < MIN_FORCE:
            return False
        if cur_len > MAX_TRAJ:
            return False
        return True

    chs = charges
    pchs = []
    for p in chs:
        if p.value == 1:
            pchs.append(p)
    amount = len(pchs)
    frame = ch_map.get_size()
    step = 0.5
    cur_ch = 0
    cur_pos = [0, 0]
    round_pos = [0, 0]
    cur_len = 0
    inside = True
    force = 1
    proc = 0
    if amount:
        proc_incr = 100/amount/SAMP_PER_CH
        tracing = True
    else:
        proc_incr = 100
        tracing = False
    if tracing:
        cur_pos = launch
        cur_len = 0
        force = 1
        while check_appr() and tracing:
            if inside:
                surface.set_at((round_pos[0], round_pos[1]), GREY)
            tens = tensity(chs, cur_pos[0], cur_pos[1])
            force = tens.length()
            koeff = step / force
            cur_pos[0] += koeff * tens.x
            cur_pos[1] += koeff * tens.y
            cur_len += step
        #proc += proc_incr
        screen.blit(surface, (0, 0))
        pgm.display.update()
        return True
    else:
        return False
