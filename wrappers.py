import gym
import numpy as np
from gym import spaces

class SuperMarioKartRewardWrapper(gym.RewardWrapper):

    def __init__(self, env: gym.Env):
        gym.RewardWrapper.__init__(self, env)
        self.previous_reward = None

    def reward(self, reward: float) -> float:
        """Just return current reward for now"""
        return reward

class SuperMarioKartObservationWrapper(gym.ObservationWrapper):

    def __init__(self, env: gym.Env, width: int = 84, height: int = 84):
        gym.ObservationWrapper.__init__(self, env)
        self.width = width
        self.height = height

    def observation(self, frame: np.ndarray):
        return frame


