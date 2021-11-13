import random
import torch
import numpy as np

# CONSTANTS
SEED = 123

# Setting randomness seeds
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)

# TODO: model class?


def inference(image_arr):
    return np.array([0,0,0,0])