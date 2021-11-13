"""
Helper for interacting with and receiving states of environment

Environment Description: Virtual pinball environment with 2 flippers, a ball, and a few obstacles.
    The goal of the game is to 1) maximize the time the ball is in play and 2) maximize the game's score

Source: Virtual pinball game based off https://github.com/LudoLogical/pinball-game.git
    Credit to author, LudoLogical, for base environment.

Observation Space:
    Type: NumPy Array (Display Width, Display Height, Color Channels)
        The observation space returns an array representing the image of the game state.
        All entries are between [0, 256]

Action Space:
    Type: NumPy Array (4)
    Num        Action
    0          Idle
    1          Fire Left Flipper
    2          Fire Right Flipper
    3          Fire Both Flippers

Reward:
    Mode 1: Agent is rewarded 1 for every second the ball is still in play
    Mode 2: Agent is rewarded with pinball scoring methods


"""

import pygame
import constants
import numpy as np
from numpy.typing import NDArray


def observation_space(display):
    string_image = pygame.image.tostring(display, 'RGB')
    tmp_surf = pygame.image.fromstring(string_image, (constants.gameW, constants.gameH), 'RGB')
    image_arr = pygame.surfarray.array3d(tmp_surf)

    return image_arr


def take_action(action_arr: NDArray):
    action = np.argmax(action_arr)
