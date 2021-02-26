import retro
import os
import numpy as np
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv, VecCheckNan, VecNormalize
from stable_baselines3.ppo import PPO, MlpPolicy, CnnPolicy
from stable_baselines3.common.atari_wrappers import WarpFrame
from wrappers import TetrisDiscretizer, SuperMarioKartDiscretizer, FzeroDiscretizer, SuperMarioKartObservationWrapper
import time
from train_ppo_refactor import get_env
from utils import code_location


game = "SuperMarioKart-Snes"
scenario = os.path.join(code_location, "scenarios", game, "custom_rewards.json")
state = os.path.join(retro.data.DATA_PATH, "data", "contrib", game, "MarioCircuit1.GP.50cc.1P.Luigi.Start.state")
model_name = os.path.join(code_location, "models", "ppo-" + game + "_final")


env = get_env(game, state, scenario)
env = DummyVecEnv([lambda: env])
model = PPO.load(model_name)
model.set_env(env)

while True:
    obs = env.reset()
    cumulative_reward = 0
    while True:
        action, _states = model.predict(obs)
        obs, rewards, dones, info = env.step(action)
        print("Step reward: {}".format(rewards))
        cumulative_reward = np.sum(rewards) + cumulative_reward
        env.render()
        if np.any(dones):
            print("Cumulative reward: {}".format(cumulative_reward))
            time.sleep(1)
            break