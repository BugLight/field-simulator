import sys
sys.path.append('..')
from physics import Vector2D
import pygame as pgm
#from time import clock as clc
from math import sin, cos
from physics.charge import Charge, tensity
from physics.consts import MIN_FORCE, MAX_TRAJ, QRAD, PCOL, NCOL, GREY, twopi

class render():
    def __init__(self, charges, ch_map, surface):
        self.chs = charges
        self.pchs = []
        for p in self.chs:
            if p.value == 1:
                self.pchs.append(p)
        self.amount = len(self.pchs)
        self.surf = surface
        self.map = ch_map
        self.frame = self.surf.get_size()
        self.step = 0.5
        self.samp_per_ch = 36
        self.ang_incr = twopi/self.samp_per_ch
        self.proc = 0
        self.proc_incr = 100/self.amount/self.samp_per_ch
        self.cur_ch = 0
        self.cur_ang = -self.ang_incr
        self.cur_pos = [0, 0]
        self.round_pos = [0, 0]
        self.cur_len = 0
        self.inside = True
        self.force = 1
        if self.amount:
            self.tracing = True
        else:
            self.tracing = False
    def check_appr(self):
        self.round_pos = [round(self.cur_pos[0]), round(self.cur_pos[1])]
        if (0 <= self.round_pos[0] < self.frame[0] and
            0 <= self.round_pos[1] < self.frame[1]):
            self.inside = True
            color = self.map.get_at(self.round_pos)
            if color == PCOL or color == NCOL:
                return False
        else:
            self.inside = False
        if self.force < MIN_FORCE:
            return False
        if self.cur_len > MAX_TRAJ:
            return False
        '''
        for q in self.chs:
            dx = q.x - self.cur_pos[0]
            dy = q.y - self.cur_pos[1]
            dist_sq = dx * dx + dy * dy
            if dist_sq <= APPR_TOL_SQ or dist_sq > MAX_FAR_SQ:
                return False
        '''
        return True
    def trace(self):
        if self.tracing:
            if self.cur_ang < twopi:
                self.cur_pos[0] = self.pchs[self.cur_ch].x - (QRAD+1) * cos(self.cur_ang)
                self.cur_pos[1] = self.pchs[self.cur_ch].y - (QRAD+1) * sin(self.cur_ang)
                self.cur_ang += self.ang_incr
            else:
                self.cur_ang = 0
                self.cur_ch += 1
                if self.cur_ch == self.amount:
                    self.tracing = 0
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
            return True
        else:
            return False
