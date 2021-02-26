import retro
import os
from train_ppo_refactor import get_env
import numpy
from utils import code_location


game = "SuperMarioKart-Snes"
scenario = os.path.join(code_location, "scenarios", game, "custom_rewards.json")
state = os.path.join(retro.data.DATA_PATH, "data", "contrib", game, "MarioCircuit1.GP.50cc.1P.Luigi.Start.state")

filename = "best_acts.txt"

with open(filename, "r") as f:
    acts = f.readlines()
acts = [int(x) for x in acts]
env = get_env(game, state, scenario)
env.reset()
cumulative_reward = 0

for k in acts:
    obs, rew, done, info = env.step(k)
    cumulative_reward += rew
    env.render()
    print("Reward: {}".format(rew))
    if done:
        print("Done. Total reward: {}".format(cumulative_reward))
        break

