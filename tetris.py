#!/usr/bin/env python

import sys
import time
import random
import curses

N = 12
M = 25

class Canvas:
    def __init__(self):
        self.mScreen = None

    def init(self):
        self.mBuffer = []
        for i in xrange(M):
            line = []
            for j in xrange(N):
                line.append(0)
            self.mBuffer.append(line)
        self.mScreen = curses.initscr()
        # curses.curs_set(2)
        self.mScreen.nodelay(1)
        self.mScreen.keypad(1)
    
    def finish(self):
        if None != self.mScreen:
            curses.endwin()
            self.mScreen = None

    def fillRandom(self):
        for i in xrange(M):
            for j in xrange(N):
                self.mBuffer[i][j] = random.randint(0, 1)
     
    def draw(self):
        for i in xrange(M):
            self.mScreen.addch(i + 1, 0, '|')
            self.mScreen.addch(i + 1, N + 1, '|')
        for i in xrange(N):
            self.mScreen.addch(0, i + 1, '-')
            self.mScreen.addch(M + 1, i + 1, '-')
        for i in xrange(M):
            for j in xrange(N):
                self.mScreen.addch(i + 1, j + 1, '*' if 0 != self.mBuffer[i][j] else ' ')
        self.mScreen.refresh()

    def read(self):
        key = self.mScreen.getch()
        while curses.ERR != self.mScreen.getch():
            pass
        return key

masksH = [
            [ [1, 1, 1, 1] ] ,
            [ [1, 1], [1, 1] ],
            [ [0, 1, 1], [1, 1, 0]],
            [ [1, 1, 0], [0, 1, 1]],
            [ [1, 0, 0], [1, 1, 1]],
            [ [1, 1, 1], [1, 0, 0]]
         ]

masksV = []
for mask in masksH:
    newMask = []
    for i in xrange(len(mask[0])):
        newMask.append([])
        for j in xrange(len(mask)):
            newMask[i].append(mask[j][len(mask[0]) - i - 1])
    masksV.append(newMask)

masks = [masksH, masksV]

class Scene:
    def __init__(self):
        self.mBuffer = []
        for i in xrange(M):
            line = []
            for j in xrange(N):
                line.append(0)
            self.mBuffer.append(line)
        self.newFigure()
        self.mScore = 0

    def newFigure(self):
        self.mF = random.randint(0, len(masks[0]) - 1)
        self.mRot = random.randint(0, 1)
        self.mFX = N/2
        self.mFY = M - len(self.getMask())

    def getMask(self):
        return masks[self.mRot][self.mF]

    def render(self, canvas):
        for i in xrange(M):
            for j in xrange(N):
                canvas.mBuffer[M - i - 1][j] = self.mBuffer[i][j]
        mask = self.getMask()
        for line in xrange(len(mask)):
            for j in xrange(len(mask[line])):
                if mask[line][j]:
                    canvas.mBuffer[M - self.mFY - 1 - line][self.mFX + j] = 1
        canvas.mScreen.addstr(M + 5, 0, str(self.mScore))

    def freezeFigure(self):
        mask = self.getMask()
        for line in xrange(len(mask)):
            for j in xrange(len(mask[line])):
                if mask[line][j]:
                    self.mBuffer[self.mFY + line][self.mFX + j] = 1
        for i in xrange(M):
            j = 0
            while j < N and self.mBuffer[i][j] == 1:
                j += 1
            if j == N:
                del self.mBuffer[i]
                line = []
                for i in xrange(N):
                    line.append(0)
                self.mBuffer.append(line)
                self.mScore += 1

    def hit(self):
        mask = self.getMask()
        if self.mFY <= 0:
            return True
        self.mFY -= 1
        try:
            for line in xrange(len(mask)):
                for j in xrange(len(mask[line])):
                    if self.mBuffer[self.mFY + line][self.mFX + j] == 1 and mask[line][j] == 1:
                        return True
            return False
        finally:
            self.mFY += 1

    def update(self, keyInput):
        if curses.KEY_UP == keyInput:
            if not self.hit():
                self.mRot = 1 - self.mRot
                if self.hit():
                    self.mRot = 1 - self.mRot
        if curses.KEY_LEFT == keyInput:
            self.mFX -= 1
        if curses.KEY_RIGHT == keyInput:
            self.mFX += 1
        if curses.KEY_DOWN == keyInput:
            if not self.hit():
                self.mFY -= 1
                while not self.hit():
                    self.mFY -= 1
                self.mFY += 1
        if self.mFX < 0:
            self.mFX = 0
        mask = self.getMask()
        if self.mFX > N - len(mask[0]):
            self.mFX = N - len(mask[0])
        if self.hit():
            self.freezeFigure()
            self.newFigure()
            if self.hit():
                return False
        self.mFY -= 1
        return True

c = Canvas()
try:
    c.init()
    s = Scene()
    while True:
        s.render(c)
        if not s.update( c.read() ):
            c.finish()
            print "Final score: " + str(s.mScore)
            sys.exit(0)
        c.draw()
        time.sleep(0.5)
finally:
    c.finish()
