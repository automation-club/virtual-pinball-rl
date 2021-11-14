import random
import torch
from torch import nn
import numpy as np
from collections import deque
import config

# CONSTANTS
SEED = config.RANDOM_SEED

# Setting randomness seeds
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)


# TODO: model class?

class DQNAgent:
    def __init__(self):
        self.memory = deque(maxlen=config.MAX_MEMORY_LEN)

        self.main_model = None
        self.target_model = None


def inference(image_arr):
    return np.array([0, 0, 0, 0])


class DQNNetwork(nn.Module):
    def __init__(self):
        super(DQNNetwork, self).__init__()

