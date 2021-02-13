import retro
import os
from baselines.common.vec_env import SubprocVecEnv
from utils import TetrisDiscretizer
from stable_baselines import PPO2, DQN
from baselines.common import models
from baselines.common.retro_wrappers import make_retro, wrap_deepmind_retro
from baselines.ppo2 import ppo2
from baselines.bench import Monitor
from stable_baselines.deepq.policies import MlpPolicy


def train_agent(game, state, scenario, network_type="cnn"):
    def make_env():
        env = make_retro(game=game,
                         state=state,
                         scenario=scenario,
                         inttype=retro.data.Integrations.CONTRIB)
        env = TetrisDiscretizer(env)
        env = Monitor(env, allow_early_resets=True, filename="fu")
        return env
    savefile_name = network_type + "_" + game
    env = make_env()
    model = DQN(MlpPolicy, env, verbose=2, tensorboard_log="C:\\Projects\\OpenAI Games\\retro-gym-hacking\\tb_logs")
    model.learn(total_timesteps=25000)
    return model


if __name__ == "__main__":
    game = "Tetris-Nes"
    state = "C:\\Users\\joncocks\\anaconda3\\envs\\retro_ai\\Lib\\site-packages\\retro\\data\\contrib\\Tetris-Nes\\Type.A.level.0.mid.state"
    scenario = "C:\\Projects\\OpenAI Games\\retro-gym-hacking\\scenarios\\custom_rewards.json"
    model = train_agent(game, state, scenario, network_type="dqn")




