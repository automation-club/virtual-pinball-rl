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
    Whichever index is non-zero is the course of action decided by the RL Agent
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
import config
import numpy as np
from numpy.typing import NDArray

# Tells flipper.py which flippers are activated
flipper_state = None


def make_observation(display):
    string_image = pygame.image.tostring(display, 'RGB')
    tmp_surf = pygame.image.fromstring(string_image, (config.gameW, config.gameH), 'RGB')
    image_arr = pygame.surfarray.array3d(tmp_surf)

    return image_arr


def take_action(observation):
    global flipper_state
    # TODO: Implement RL inference
    x = np.array([0, 0, 0, 0])
    flipper_state = np.argmax(x)


def get_flipper_state():
    global flipper_state
    return flipper_state
