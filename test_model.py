import retro
import os
import numpy as np
from stable_baselines import PPO2
from stable_baselines.common.policies import CnnPolicy, MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from utils import TetrisDiscretizer, SuperMarioKartDiscretizer, FzeroDiscretizer
import time


# game = "NHLHockey94-Genesis"
# scenario = "C:\\Projects\\OpenAI Games\\retro-gym-hacking\\scenarios\\NHLHockey94-Genesis\\custom_rewards.json"
# state = "C:\\Users\\joncocks\\anaconda3\\envs\\retro_ai\\Lib\\site-packages\\retro\\data\\contrib\\NHLHockey94-Genesis\\LAK.MTL.Regular.1P.fastclock.state"

# game = "Tetris-nes"
# scenario = "C:\\Projects\\OpenAI Games\\retro-gym-hacking\\scenarios\\Tetris-Nes\\custom_rewards.json"
# state = "C:\\Users\\joncocks\\anaconda3\\envs\\retro_ai\\Lib\\site-packages\\retro\\data\\contrib\\Tetris-Nes\\Type.A.level.9.start.state"

game = "SuperMarioKart-Snes"
scenario = "C:\\Projects\\OpenAI Games\\retro-gym-hacking\\scenarios\\SuperMarioKart-Snes\\custom_rewards.json"
state = "C:\\Users\\joncocks\\anaconda3\\envs\\retro_ai\\Lib\\site-packages\\retro\\data\\contrib\\SuperMarioKart-Snes\\MarioCircuit1.GP.50cc.1P.Luigi.Start.state"

# game = "Fzero-Snes"
# scenario = "C:\\Users\\joncocks\\anaconda3\\envs\\retro_ai\\Lib\\site-packages\\retro\\data\\contrib\\Fzero-Snes\\scenario.json"
# state = "C:\\Users\\joncocks\\anaconda3\\envs\\retro_ai\\Lib\\site-packages\\retro\\data\\contrib\\Fzero-Snes\\practice.mutecity.bluefalcon.norival.start.state"

model_name = game + "-ppo2"



env = retro.make(game,
                 state=state,
                 scenario=scenario,
                 inttype=retro.data.Integrations.CONTRIB,
                 obs_type=retro.Observations.IMAGE)
if game == "Tetris-nes":
    env = TetrisDiscretizer(env)
elif game == "SuperMarioKart-Snes":
    env = SuperMarioKartDiscretizer(env)
elif game == "Fzero-Snes":
    env = FzeroDiscretizer(env)
env = DummyVecEnv([lambda: env])

model = PPO2.load(model_name)
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