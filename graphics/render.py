import sys
sys.path.append('..')
from physics import Vector2D
import pygame as pgm
from math import sin, cos
from physics.charge import Charge, tensity
from physics.consts import *
from .tracer import Tracer

class Render():
    def __init__(self, charges, ch_map, screen, surface):
        self.chs = charges
        self.pchs = []
        for p in self.chs:
            if p.value == 1:
                self.pchs.append(p)
        self.amount = len(self.pchs)
        self.screen = screen
        self.surf = surface
        self.map = ch_map
        self.frame = self.surf.get_size()
        self.step = 0.5
        self.cur_ch = 0
        self.cur_pos = [0, 0]
        self.round_pos = [0, 0]
        self.cur_len = 0
        self.inside = True
        self.force = 1
        self.proc = 0
        if self.amount:
            self.proc_incr = 100/self.amount/SAMP_PER_CH
            self.tracing = True
        else:
            self.proc_incr = 100
            self.tracing = False
        launches = []
        fi = 0
        while fi < twopi:
            for q in charges:
                if q.value == 1:
                    launches.append([q.x - (QRAD+1) * cos(fi), q.x - (QRAD+1) * sin(fi)])
            fi += ANG_INCR
        workers = [Tracer(self.trace) for i in range(WORKERS_COUNT)]
        for i in range(len(launches)):
            workers[i % WORKERS_COUNT].put(launches[i])
        for w in workers:
            w.start()


    def check_appr(self):
        self.round_pos = [round(self.cur_pos[0]), round(self.cur_pos[1])]
        if (0 <= self.round_pos[0] < self.frame[0] and
            0 <= self.round_pos[1] < self.frame[1]):
            self.inside = True
            print(self.round_pos)
            color = self.map.get_at(self.round_pos)
            if color == PCOL or color == NCOL:
                return False
        else:
            self.inside = False
        if self.force < MIN_FORCE:
            return False
        if self.cur_len > MAX_TRAJ:
            return False
        return True
    def trace(self, launch):
        if self.tracing:
            self.cur_pos = launch
            self.cur_len = 0
            self.force = 1
            while self.check_appr() and self.tracing:
                if self.inside:
                    self.surf.set_at((self.round_pos[0], self.round_pos[1]), GREY)
                tens = tensity(self.chs, self.cur_pos[0], self.cur_pos[1])
                self.force = tens.length()
                koeff = self.step / self.force
                self.cur_pos[0] += koeff * tens.x
                self.cur_pos[1] += koeff * tens.y
                self.cur_len += self.step
            self.proc += self.proc_incr
            self.screen.blit(self.surf, (0, 0))
            return True
        else:
            return False
