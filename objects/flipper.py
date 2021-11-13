import pygame, math, config, copy, keyboard
import reinforcement_learning.environment_helper as env_helper
from pygame import gfxdraw
from logic import collisions
from logic.graphics import sortByX, sortByY
from objects.rect import Rect

class Flipper(Rect):
    def __init__(self,x,y,w,h,angle,activeAngle,color,name="flipper"):
        super().__init__(x,y,w,h,color,None,[0,0],name)

        self.pivotX = x-35 # pivotY = y

        self.angle = angle
        self.activeAngle = activeAngle
        self.power = 12

        self.inactiveRecent = 0
        self.cooldown = 0
        self.cooldownMax = 3

        self.angleCoords = self.prepCoords(angle)
        self.activeAngleCoords = self.prepCoords(activeAngle)

    def prepCoords(self, theta):
        coOrds = [[self.x - self.w/2, self.y - self.h/2],
                [self.x + self.w/2, self.y - self.h/2],
                [self.x + self.w/2, self.y + self.h/2],
                [self.x - self.w/2, self.y + self.h/2]]

        if self.w > self.h:
            rotateX = self.x - (self.w/2 - self.h/2)
            rotateY = self.y
        else:
            rotateX = self.x
            rotateY = self.y - (self.h/2 - self.w/2)

        for n in range(0,len(coOrds)):

            coOrds[n][0] -= rotateX
            coOrds[n][1] -= rotateY

            xnew = coOrds[n][0] * math.cos(theta) - coOrds[n][1] * math.sin(theta)
            ynew = coOrds[n][0] * math.sin(theta) + coOrds[n][1] * math.cos(theta)

            coOrds[n] = [xnew + rotateX, ynew + rotateY]

        return coOrds

    def is_active(self):
        if config.AUTONOMOUS_MODE:
            if self.name == "L" and (env_helper.get_flipper_state() == 1 or env_helper.get_flipper_state() == 3):
                return True
            if self.name == "R" and (env_helper.get_flipper_state() == 2 or env_helper.get_flipper_state() == 3):
                return True
            else:
                return False
        else:
            if (self.name == "L" and keyboard.leftFlipper()) or (self.name == "R" and keyboard.rightFlipper()):
                return True
            else:
                return False

    def currentCoords(self):
        if self.is_active():
            return self.activeAngleCoords
        else:
            return self.angleCoords

    def getAngle(self):
        if self.is_active():
            return self.activeAngle
        else:
            return self.angle

    def getHighestPoints(self):
        temp = copy.deepcopy(self.angleCoords)
        temp.sort(key=sortByY)
        return temp[0], temp[1]

    def draw(self, ctx):

        if self.is_active():
            gfxdraw.filled_polygon(ctx, self.activeAngleCoords, self.color)
            gfxdraw.aapolygon(ctx, self.activeAngleCoords, self.color)
        else:
            gfxdraw.filled_polygon(ctx, self.angleCoords, self.color)
            gfxdraw.aapolygon(ctx, self.angleCoords, self.color)

    def go(self, ctx, ball):
        if self.is_active():
            if self.inactiveRecent > 0 and self.cooldown == 0:
                ball.checkFlipperHit(self)
                self.inactiveRecent -= 1
                self.cooldown = self.cooldownMax
        else:
            self.inactiveRecent = 3
        if self.cooldown > 0:
            self.cooldown -= 1
        super().go(ctx)

