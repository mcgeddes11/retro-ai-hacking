import gym
import numpy as np

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
        action_space = [["B"], ["B", "LEFT"], ["B", "RIGHT"]]
        super().__init__(env=env, combos=action_space)

class FzeroDiscretizer(Discretizer):
    def __init__(self, env):
        super().__init__(env=env, combos=[['B'], ['LEFT', 'B'], ['RIGHT', 'B']])