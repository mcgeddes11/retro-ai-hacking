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

# This script uses a set of pre-trained models to complete (and probably win) the 50cc mushroom cup

# Define game and scenario
game = "SuperMarioKart-Snes"
scenario = os.path.join(code_location, "scenarios", game, "custom_rewards.json")

# Load the starting state
first_course = "GhostHouse1"
state = os.path.join(retro.data.DATA_PATH, "data", "contrib", game, "{}.GP.50cc.1P.Koopa.Start.state".format(first_course))

# Define model transitions as courses change
course_model_map = {7: "GhostHouse1",
                    19: "GhostHouse1",
                    16: "GhostHouse1",
                    17: "GhostHouse1",
                    15: "GhostHouse1"}

# Model name stub
stub = os.path.join(code_location, "models", "ppo_SuperMarioKart-Snes_Koopa_50cc_{}_final")

# Load the initial model for the first course
model_name = stub.format(first_course)

# Create the game environment
env = get_env(game, state, scenario)

# Record a movie of the output if requested
record_movie = False
if record_movie:
    moviepath = "movie.mp4"
    env = MovieRecordWrapper(env, savedir=moviepath)

# Vectorize the environment
env = DummyVecEnv([lambda: env])

# Load the model and set the environment
model = PPO.load(model_name)
model.set_env(env)

# Reset the environment
obs = env.reset()

# Set the last_course to the first course we're on, MarioCircuit1
last_course = 7

while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)

    # get the course code extracted from RAM
    # Need to get first element as we're only using one environment
    current_course = info[0]["track_code"]

    # Load the next model if we've changed to a new course

    if last_course != current_course and current_course in course_model_map.keys():
        model_name = stub.format(course_model_map[current_course])
        model = PPO.load(model_name)
        model.set_env(env)
        last_course = current_course

    print("Step reward: {}".format(rewards))
    # cumulative_reward = np.sum(rewards) + cumulative_reward
    env.render()
    # if np.any(dones):
    #     # print("Cumulative reward: {}".format(cumulative_reward))
    #     time.sleep(1)
    #     break