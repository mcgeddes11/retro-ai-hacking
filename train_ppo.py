import retro
import os
from stable_baselines.common.vec_env import SubprocVecEnv
from stable_baselines.common.policies import CnnPolicy, MlpPolicy
from utils import TetrisDiscretizer
from stable_baselines import PPO2

from stable_baselines.bench import Monitor


def make_env():
    env = retro.make(game=game,
                     state=state,
                     scenario=scenario,
                     inttype=retro.data.Integrations.CONTRIB)
    # env = TetrisDiscretizer(env)
    # env = wrap_deepmind_retro(env)
    env = Monitor(env, allow_early_resets=True, filename="fu")
    return env


if __name__ == "__main__":
    # game = "Tetris-Nes"
    # state = "C:\\Users\\joncocks\\anaconda3\\envs\\retro_ai\\Lib\\site-packages\\retro\\data\\contrib\\Tetris-Nes\\Type.A.level.9.start.state"
    # scenario = "C:\\Projects\\OpenAI Games\\retro-gym-hacking\\scenarios\\Tetris-Nes\\custom_rewards.json"
    game = "NHLHockey94-Genesis"
    scenario = "C:\\Projects\\OpenAI Games\\retro-gym-hacking\\scenarios\\NHLHockey94-Genesis\\custom_rewards.json"
    state = "C:\\Users\\joncocks\\anaconda3\\envs\\retro_ai\\Lib\\site-packages\\retro\\data\\contrib\\NHLHockey94-Genesis\\LAK.MTL.Regular.1P.fastclock.state"
    savefile_name = game + "_model"
    venv = SubprocVecEnv([make_env] * 4)
    if savefile_name is not None and os.path.exists(savefile_name):
        model = PPO2.load(savefile_name)
    else:
        model = PPO2(CnnPolicy,
                     venv,
                     n_steps=128,
                     nminibatches=4,
                     lam=0.95,
                     gamma=0.99,
                     noptepochs=4,
                     ent_coef=.01,
                     learning_rate=lambda f: f * 2.5e-3,
                     cliprange=0.2,
                     cliprange_vf=-1,
                     verbose=1
                     )
    model.learn(total_timesteps=200000,log_interval=1)
    model.save(savefile_name)




