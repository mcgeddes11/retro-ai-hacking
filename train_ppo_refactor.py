import retro
from uuid import uuid4
import os
import numpy as np
from stable_baselines3.ppo import PPO, MlpPolicy, CnnPolicy
from stable_baselines3.a2c import A2C
from stable_baselines3.common.atari_wrappers import WarpFrame
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv, VecCheckNan, VecNormalize
from wrappers import TetrisDiscretizer, SuperMarioKartDiscretizer, FzeroDiscretizer, RewardScaler
from retro.examples.brute import Frameskip, TimeLimit, Brute
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import CheckpointCallback
from environments import SuperMarioKartEnv
from utils import code_location


def get_env(game, state, scenario):
    if game == "SuperMarioKart-Snes":
        env = SuperMarioKartEnv(game, state, scenario, inttype=retro.data.Integrations.CONTRIB)
    else:
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
    env = Frameskip(env)
    env = RewardScaler(env)
    env = Monitor(env)
    return env



if __name__ == "__main__":

    # game = "Tetris-Nes"
    # scenario = "C:\\Projects\\OpenAI Games\\retro-ai-hacking\\scenarios\\Tetris-Nes\\custom_rewards.json"
    # state = "C:\\Users\\joncocks\\anaconda3\\envs\\retro_ai_3\\Lib\\site-packages\\retro\\data\\contrib\\Tetris-Nes\\Type.A.level.9.start.state"

    # game = "NHLHockey94-Genesis"
    # scenario = "C:\\Projects\\OpenAI Games\\retro-ai-hacking\\scenarios\\NHLHockey94-Genesis\\custom_rewards.json"
    # state = "C:\\Users\\joncocks\\anaconda3\\envs\\retro_ai_3\\Lib\\site-packages\\retro\\data\\contrib\\NHLHockey94-Genesis\\LAK.MTL.Regular.1P.fastclock.state"

    game = "SuperMarioKart-Snes"
    scenario = "C:\\Projects\\OpenAI Games\\retro-ai-hacking\\scenarios\\SuperMarioKart-Snes\\custom_rewards.json"
    state = "C:\\Users\\joncocks\\anaconda3\\envs\\retro_ai_3\\Lib\\site-packages\\retro\\data\\contrib\\SuperMarioKart-Snes\\MarioCircuit1.GP.50cc.1P.Luigi.Start.state"

    # game = "Fzero-Snes"
    # scenario = "C:\\Users\\joncocks\\anaconda3\\envs\\retro_ai_3\\Lib\\site-packages\\retro\\data\\contrib\\Fzero-Snes\\scenario.json"
    # state = "C:\\Users\\joncocks\\anaconda3\\envs\\retro_ai_3\\Lib\\site-packages\\retro\\data\\contrib\\Fzero-Snes\\practice.mutecity.bluefalcon.norival.start.state"

    experiment_id = str(uuid4())

    n_cpus = 8
    env = SubprocVecEnv([lambda: get_env(game, state, scenario) for i in range(n_cpus)])
    # env = DummyVecEnv([lambda: get_env(game, state, scenario)])
    # env = VecNormalize(env, norm_obs=True, norm_reward=False)
    env = VecCheckNan(env, raise_exception=True)

    # Create a callback to save every n timesteps
    prefix = "ppo_" + game + "_" + experiment_id
    checkpoint_callback = CheckpointCallback(save_freq=100000, save_path="C:\\Projects\\OpenAI Games\\retro-ai-hacking\\models", name_prefix=prefix)

    savefile_name = prefix + "_final"

    savefile_name = os.path.join("C:\\Projects\\OpenAI Games\\retro-ai-hacking\\models", savefile_name)

    model = PPO(CnnPolicy,
                 env,
                 verbose=1,
                 n_steps=128,
                 n_epochs=3,
                 learning_rate=2.5e-4,
                 batch_size=32,
                 ent_coef=0.01,
                 vf_coef=1.0,
                 tensorboard_log="C:\\Projects\\OpenAI Games\\retro-ai-hacking\\tb_logs")
    model.learn(total_timesteps=1000000, callback=checkpoint_callback)
    model.save(savefile_name)

