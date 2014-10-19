#!/usr/bin/env python

import time
import random
import curses

N = 10
M = 40

class Canvas:
    def __init__(self):
        self.mBuffer = []
        for i in xrange(M):
            line = []
            for j in xrange(N):
                line.add(0)
            self.mBuffer.add(line)
        self.mPad = curses.newpad(M, N)

    def fillRandom(self):
        for i in xrange(M):
            for j in xrange(N):
                self.mBuffer[i][j] = random.randint() & 1
     
    def draw(self):
        for i in xrange(M):
            for j in xrange(N):
                self.mPad.addch(i, j, "*" if 0 != self.mBuffer[i][j] else " ")
        self.mPad.refresh(0, 0, M, N)

c = Canvas()
while True:
    c.fillRandom()
    c.draw()
    time.sleep(1)
