import retro
import os
import numpy as np
from stable_baselines3.ppo import PPO, MlpPolicy, CnnPolicy
from stable_baselines3.a2c import A2C
from stable_baselines3.common.atari_wrappers import WarpFrame
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv, VecCheckNan, VecNormalize
from utils import TetrisDiscretizer, SuperMarioKartDiscretizer, FzeroDiscretizer
from stable_baselines3.common.monitor import Monitor

# game = "Tetris-Nes"
# scenario = "C:\\Projects\\OpenAI Games\\retro-gym-hacking\\scenarios\\Tetris-Nes\\custom_rewards.json"
# state = "C:\\Users\\joncocks\\anaconda3\\envs\\retro_ai_3\\Lib\\site-packages\\retro\\data\\contrib\\Tetris-Nes\\Type.A.level.9.start.state"

# game = "NHLHockey94-Genesis"
# scenario = "C:\\Projects\\OpenAI Games\\retro-gym-hacking\\scenarios\\NHLHockey94-Genesis\\custom_rewards.json"
# state = "C:\\Users\\joncocks\\anaconda3\\envs\\retro_ai_3\\Lib\\site-packages\\retro\\data\\contrib\\NHLHockey94-Genesis\\LAK.MTL.Regular.1P.fastclock.state"

game = "SuperMarioKart-Snes"
scenario = "C:\\Projects\\OpenAI Games\\retro-gym-hacking\\scenarios\\SuperMarioKart-Snes\\custom_rewards.json"
state = "C:\\Users\\joncocks\\anaconda3\\envs\\retro_ai_3\\Lib\\site-packages\\retro\\data\\contrib\\SuperMarioKart-Snes\\MarioCircuit1.GP.50cc.1P.Luigi.Start.state"

# game = "Fzero-Snes"
# scenario = "C:\\Users\\joncocks\\anaconda3\\envs\\retro_ai_3\\Lib\\site-packages\\retro\\data\\contrib\\Fzero-Snes\\scenario.json"
# state = "C:\\Users\\joncocks\\anaconda3\\envs\\retro_ai_3\\Lib\\site-packages\\retro\\data\\contrib\\Fzero-Snes\\practice.mutecity.bluefalcon.norival.start.state"

env = retro.make(game,
                 state=state,
                 scenario=scenario,
                 inttype=retro.data.Integrations.CONTRIB,
                 obs_type=retro.Observations.IMAGE)
if game == "Tetris-Nes":
    env = TetrisDiscretizer(env)
elif game == "SuperMarioKart-Snes":
    env = SuperMarioKartDiscretizer(env)
elif game == "Fzero-Snes":
    env = FzeroDiscretizer(env)
env = WarpFrame(env)
env = Monitor(env)

# n_cpus = 4
# env = SubprocVecEnv([lambda: env for i in range(n_cpus)])
env = DummyVecEnv([lambda: env])
env = VecNormalize(env, norm_obs=True, norm_reward=False)
env = VecCheckNan(env, raise_exception=True)

savefile_name = game + "-ppo"
if os.path.exists(savefile_name):
    model = PPO.load(savefile_name)
    model.set_env(env)
else:
    model = PPO(CnnPolicy,
                 env,
                 # verbose=1,
                 # n_steps=128,
                 # learning_rate=5.0e-4,
                 # ent_coef=0.2,
                 tensorboard_log="C:\\Projects\\OpenAI Games\\retro-gym-hacking\\tb_logs")
model.learn(total_timesteps=100000)
model.save(savefile_name)

