import retro
import os
import numpy as np
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv, VecCheckNan, VecNormalize
from stable_baselines3.ppo import PPO, MlpPolicy, CnnPolicy
from stable_baselines3.common.atari_wrappers import WarpFrame
from wrappers import TetrisDiscretizer, SuperMarioKartDiscretizer, FzeroDiscretizer, MovieRecordWrapper
import time
from train_ppo_refactor import get_env
from utils import code_location

 #SUPER MARIO KART
# game = "SuperMarioKart-Snes"
# scenario = os.path.join(code_location, "scenarios", game, "custom_rewards.json")
# state = os.path.join(retro.data.DATA_PATH, "data", "contrib", game, "MarioCircuit1.GP.100cc.1P.DK.Start.state")
# state = os.path.join(retro.data.DATA_PATH, "data", "contrib", game, "MarioCircuit1.GP.50cc.1P.Koopa.Start.state")
# state = os.path.join(retro.data.DATA_PATH, "data", "contrib", game, "DonutPlains1.GP.50cc.1P.Koopa.Start.state")
# state = os.path.join(retro.data.DATA_PATH, "data", "contrib", game, "GhostHouse1.GP.50cc.1P.Koopa.Start.state")
# state = os.path.join(retro.data.DATA_PATH, "data", "contrib", game, "GhostHouse1.TimeTrial.50cc.1P.Koopa.Start.state")
# state = os.path.join(retro.data.DATA_PATH, "data", "contrib", game, "MarioCircuit2.GP.50cc.1P.Koopa.Start.state")

# SMASH TV
game = "SmashTV-Snes"
scenario = os.path.join(code_location, "scenarios", game, "custom_rewards.json")
state = os.path.join(retro.data.DATA_PATH, "data", "contrib", game, "1P.Normal.Arena1.state")

# model_name = os.path.join(code_location, "models", "ppo_SuperMarioKart-Snes_Koopa_50cc_MarioCircuit1_final")
model_name = os.path.join(code_location, "models", "ppo_SmashTV-Snes_57644741-87b6-4a0c-a102-37f0656e52a0_final")


env = get_env(game, state, scenario)
# Record a movie of the output
record_movie = False
if record_movie:
    moviepath = "movie.mp4"
    env = MovieRecordWrapper(env, savedir=moviepath)


env = DummyVecEnv([lambda: env])
model = PPO.load(model_name)
model.set_env(env)

obs = env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    print("Step reward: {}".format(rewards))
    # cumulative_reward = np.sum(rewards) + cumulative_reward
    env.render()
    if np.any(dones):
        # print("Cumulative reward: {}".format(cumulative_reward))
        time.sleep(1)
        break