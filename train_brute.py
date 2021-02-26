import retro
import os
from retro.examples.brute import Frameskip, TimeLimit, Brute, EXPLORATION_PARAM
from wrappers import TetrisDiscretizer, SuperMarioKartDiscretizer, FzeroDiscretizer
from train_ppo_refactor import get_env
from utils import code_location

game = "SuperMarioKart-Snes"
scenario = os.path.join(code_location, "scenarios", game, "custom_rewards.json")
state = os.path.join(retro.data.DATA_PATH, "data", "contrib", game, "MarioCircuit1.GP.50cc.1P.Luigi.Start.state")


max_episode_steps = 10000
timestep_limit = 1e8

env = get_env(game, state, scenario)
env = TimeLimit(env, max_episode_steps=max_episode_steps)
brute = Brute(env, max_episode_steps=max_episode_steps)
timesteps = 0
best_rew = float('-inf')
while True:
    acts, rew = brute.run(render=True)
    timesteps += len(acts)

    if rew > best_rew:
        print("new best reward {} => {}".format(best_rew, rew))
        best_rew = rew
        with open("best_acts.txt", "w") as f:
            for act in acts:
                f.write("%i\n" % act)
        # env.unwrapped.record_movie("best.bk2")
        env.reset()
        for act in acts:
            env.step(act)
        env.unwrapped.stop_record()

    if timesteps > timestep_limit:
        print("timestep limit exceeded")
        break
