import gym
import numpy as np
from gym import spaces
import cv2

class SuperMarioKartRewardWrapper(gym.RewardWrapper):

    def __init__(self, env: gym.Env):
        gym.RewardWrapper.__init__(self, env)
        self.previous_reward = None

    def reward(self, reward: float) -> float:
        """Just return current reward for now"""
        return reward

class SuperMarioKartObservationWrapper(gym.ObservationWrapper):

    def __init__(self, env: gym.Env):
        gym.ObservationWrapper.__init__(self, env)
        self.observation_space = gym.spaces.Box(low=0, high=255,
                   shape=(112,256,3), dtype=np.uint8)
    def observation(self, frame: np.ndarray):
        return frame[0:112,:,:]

    def get_map(self):
        map = np.zeros((128,128))
        for x in range(1,128):
            for y in range(1,128):
                address = 8323072+((x-1)+(y-1)*128)*1
                tile = self.env.env.data.memory.extract(address, "|i1")
                map[x-1, y-1] = tile



class RewardScaler(gym.RewardWrapper):
    """
    Bring rewards to a reasonable scale for PPO.
    This is incredibly important and effects performance
    drastically.
    """
    def __init__(self, env, scale=0.01):
        super(RewardScaler, self).__init__(env)
        self.scale = scale

    def reward(self, reward):
        return reward * self.scale

class Downsample(gym.ObservationWrapper):
    def __init__(self, env, ratio):
        """
        Downsample images by a factor of ratio
        """
        gym.ObservationWrapper.__init__(self, env)
        (oldh, oldw, oldc) = env.observation_space.shape
        newshape = (oldh//ratio, oldw//ratio, oldc)
        self.observation_space = gym.spaces.Box(low=0, high=255,
            shape=newshape, dtype=np.uint8)

    def observation(self, frame):
        height, width, _ = self.observation_space.shape
        frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
        if frame.ndim == 2:
            frame = frame[:,:,None]
        return frame

class Rgb2gray(gym.ObservationWrapper):
    def __init__(self, env):
        """
        Downsample images by a factor of ratio
        """
        gym.ObservationWrapper.__init__(self, env)
        (oldh, oldw, _oldc) = env.observation_space.shape
        self.observation_space = gym.spaces.Box(low=0, high=255,
            shape=(oldh, oldw, 1), dtype=np.uint8)

    def observation(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        return frame[:,:,None]


class MovieRecord(gym.Wrapper):
    def __init__(self, env, savedir, k):
        gym.Wrapper.__init__(self, env)
        self.savedir = savedir
        self.k = k
        self.epcount = 0

    def reset(self):
        if self.epcount % self.k == 0:
            self.env.unwrapped.movie_path = self.savedir
        else:
            self.env.unwrapped.movie_path = None
            self.env.unwrapped.movie = None
        self.epcount += 1
        return self.env.reset()


class Discretizer(gym.ActionWrapper):
    """
    Wrap a gym environment and make it use discrete actions.
    Args:
        combos: ordered list of lists of valid button combinations
    """

    def __init__(self, env, combos):
        super().__init__(env)
        assert isinstance(env.action_space, gym.spaces.MultiBinary)
        buttons = env.unwrapped.buttons
        self._decode_discrete_action = []
        for combo in combos:
            arr = np.array([False] * env.action_space.n)
            for button in combo:
                arr[buttons.index(button)] = True
            self._decode_discrete_action.append(arr)

        self.action_space = gym.spaces.Discrete(len(self._decode_discrete_action))

    def action(self, act):
        return self._decode_discrete_action[act].copy()


class TetrisDiscretizer(Discretizer):
    """
    Use Tetris-specific discrete actions
    based on https://github.com/openai/retro-baselines/blob/master/agents/sonic_util.py
    """
    def __init__(self, env):
        super().__init__(env=env, combos=[['LEFT'], ['RIGHT'], ['DOWN'], ['A'], ['B']])


class SuperMarioKartDiscretizer(Discretizer):
    def __init__(self, env):
        # action_space = [['LEFT'], ['RIGHT'], ['DOWN'], ['A'], ['B'], ['L'], ['LEFT', 'B'], ['RIGHT', 'B'],
        #                 ['LEFT','A','B'], ['RIGHT','A','B'], ['DOWN','B'], ['DOWN','A','B']]
        action_space = [['B'], ['LEFT', 'B'], ['RIGHT', 'B']]
        super().__init__(env=env, combos=action_space)


class FzeroDiscretizer(Discretizer):
    def __init__(self, env):
        super().__init__(env=env, combos=[['B'], ['LEFT', 'B'], ['RIGHT', 'B']])


