# Window will spawn in exact center
import os

import config
import math
import pygame
import pygame.camera
from pygame import gfxdraw
from win32api import GetSystemMetrics

import keyboard
import mouse
import reinforcement_learning.environment_helper as env_helper
from img import images
from logic import collisions
from objects.ball import Ball
from objects.brick import Brick
from objects.bumper import Bumper
from objects.flipper import Flipper
from objects.polygon import Polygon
from objects.rect import Rect

windowX = GetSystemMetrics(0) / 2 - config.gameW / 2
windowY = GetSystemMetrics(1) / 2 - config.gameH / 2
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (windowX, windowY)

pygame.init()
from pygame.locals import DOUBLEBUF  # FULLSCREEN

display = pygame.display.set_mode((config.gameW, config.gameH), DOUBLEBUF)

display.set_alpha(None)
pygame.display.set_caption("Pinball")
clock = pygame.time.Clock()


def listen(running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
            running = False
        # elif event.type == sounds.END_FLAG:
        #     sounds.changeMusic(sounds.overtureLoopTime)
        else:
            keyboard.listen(event)
            mouse.listen()
    return running


def main():
    # pygame.mixer.music.play()
    # midline = Rect(199,0,2,600,(0,0,0))

    running = True
    ballsLeft = 2
    state = config.TITLE_SCREEN

    playButton = Rect(config.gameW / 2 - 105, config.gameH - 200, 210, 63, None, images.playButton)
    plunger = Rect(config.gameW - 30, config.gameH - 60, 20, 60, None, images.plunger)

    ball = Ball(380, 550, 10, config.colors['ball'])

    # PREP FOR FLIPPERS
    leftX = -15 + config.gameW / 2 - 45
    rightX = 15 + config.gameW / 2 + 45 + 2 * 35
    flippers = [
        Flipper(leftX, 550, 90, 20, 5 * math.pi / 36, -5 * math.pi / 36, config.colors['flipper'], "L"),
        Flipper(rightX, 550, 90, 20, 31 * math.pi / 36, 41 * math.pi / 36, config.colors['flipper'], "R")
    ]

    # PREP FOR BASES
    leftHigh, left2ndHigh = flippers[0].getHighestPoints()
    leftXRate = math.tan(flippers[0].angle)
    leftmostTop = [0, leftHigh[1] - leftHigh[0] * leftXRate]
    leftmostBot = [0, left2ndHigh[1] - left2ndHigh[0] * leftXRate]
    rightHigh, right2ndHigh = flippers[1].getHighestPoints()
    rightXRate = -math.tan(flippers[1].angle)
    rightmostTop = [config.gameW, rightHigh[1] - (config.gameW - rightHigh[0]) * rightXRate]
    rightmostBot = [config.gameW, right2ndHigh[1] - (config.gameW - right2ndHigh[0]) * rightXRate]
    bases = [
        Polygon([leftmostTop, leftHigh, left2ndHigh, leftmostBot], flippers[0].angle, config.colors['wall']),
        Polygon([rightmostTop, rightHigh, right2ndHigh, rightmostBot], flippers[1].angle, config.colors['wall'])
    ]

    walls = [
        Rect(0, 0, config.gameW, 10, config.colors['wall']),
        Rect(0, 0, 20, config.gameH, config.colors['wall']),
        Rect(config.gameW - 40, 0, 40, config.gameH, config.colors['wall'])
    ]
    bumpers = [Bumper(60, 60), Bumper(175, 145), Bumper(265, 130), Bumper(240, 210),
               Bumper(100, 270, 50, 50, None, images.burst, "superbumper")]
    bricks = [Brick(30, 160, 95, 36, 30 + 48, 30 + 95 - 48)]

    while running:
        if not config.AUTONOMOUS_MODE:
            running = listen(running)

        if state == config.TITLE_SCREEN:
            display.blit(images.menu, (0, 0))
            playButton.go(display)
            if mouse.mouse['click'] and collisions.rectPoint(playButton, mouse.mouse['pos']):
                state = config.STAGE_ONE

        elif state == config.STAGE_ONE:

            # Game Logic
            if keyboard.controls['keySpace'] and ball.launching and ball.spd[1] == 0:
                ball.spd[1] = -14

            if keyboard.controls['keyEnter']:
                ball.reset()

            display.fill(config.colors['bg'])

            for b in bases:
                b.go(display)
            for w in walls:
                w.go(display)
            for bb in bumpers:
                bb.go(display)
            for bbb in bricks:
                bbb.go(display)

            # Flipper actions are decided here through either keyboard input or RL Agent
            observation = env_helper.make_observation(display)
            env_helper.take_action(observation)
            for f in flippers:
                f.go(display, ball)

            gfxdraw.filled_polygon(display, [[350, 0], [400, 0], [400, 50]], config.colors['releaser'])
            gfxdraw.aapolygon(display, [[350, 0], [400, 0], [400, 50]], config.colors['releaser'])

            plunger.go(display)
            display.blit(images.button, (330, 320))

            scoreTEXT = str(ballsLeft) + " | " + str(ball.score)
            scoreRender = config.muli["30"].render(scoreTEXT, True, config.colors['score'])
            scoreRECT = scoreRender.get_rect()
            scoreRECT.right = config.gameW - 60
            scoreRECT.top = 20
            display.blit(scoreRender, scoreRECT)

            ball.go(display, flippers, bases, walls, bumpers, bricks)

            if ball.y > config.gameH or ball.x < 0 or ball.x > config.gameW:
                if ballsLeft > 0:
                    ball.reset()
                    ballsLeft -= 1
                else:
                    state = config.GAME_OVER

            # Debug
            # pygame.draw.rect(ctx,constants.colors['white'],(leftX-35,550,1,1))
            # pygame.draw.rect(ctx,constants.colors['white'],(rightX-35,550,1,1))
            pygame.draw.rect(display, config.colors['white'], (flippers[0].pivotX, flippers[0].y, 1, 1))
            # midline.go(ctx)
            fpsTEXT = str(round(clock.get_fps(), 1))
            fps = config.muli["15"].render(fpsTEXT, True, config.colors['black'])
            display.blit(fps, (25, 8))

        elif state == config.GAME_OVER:
            display.blit(images.gameOver, (0, 0))
            playButton.go(display)

            scoreTEXT = str(ball.score) + " points."
            scoreRender = config.muli["30"].render(scoreTEXT, True, config.colors['score'])
            scoreRECT = scoreRender.get_rect()
            scoreRECT.center = (config.gameW / 2, config.gameH - 300)
            display.blit(scoreRender, scoreRECT)

            if mouse.mouse['click'] and collisions.rectPoint(playButton, mouse.mouse['pos']):
                state = config.STAGE_ONE
                ball.score = 0
                ballsLeft = 3

        # Update Window
        pygame.display.update()
        # input()
        clock.tick(10)

    pygame.quit()


main()
