import retro
import os
from wrappers import TetrisDiscretizer, SuperMarioKartDiscretizer, RewardScaler
from stable_baselines3.common.atari_wrappers import WarpFrame
from environments import SuperMarioKartEnv
from matplotlib import pyplot as plt
from retro.examples.brute import Frameskip, TimeLimit, Brute
from stable_baselines3.common.monitor import Monitor
from utils import code_location


def main(game, state, scenario):

    # env = retro.make(game=game, state=state, scenario=scenario, inttype=retro.data.Integrations.CONTRIB)
    env = SuperMarioKartEnv(game, state, scenario, inttype=retro.data.Integrations.CONTRIB)
    if game == "Tetris-Nes":
        env = TetrisDiscretizer(env)
    elif game == "SuperMarioKart-Snes":
        env = SuperMarioKartDiscretizer(env)
    # env = SuperMarioKartObservationWrapper(env)
    env = Frameskip(env)
    env = RewardScaler(env)
    env = Monitor(env)

    obs = env.reset()
    cumulative_reward = 0
    count = 1
    while True:
        action = env.action_space.sample()
        obs, rew, done, info = env.step(env.action_space.sample())
        print(action)
        # if rew != 0:
            # print("Reward!")
            # plt.imshow(obs)
        cumulative_reward = cumulative_reward + rew
        print("Frame count: {}; Reward: {}".format(count, rew))
        # if rew != 0:
        #     print("Info: {}".format(info))
        #     print("Reward: {}".format(rew))
        env.render()
        count +=1
        if done:
            env.reset()
    env.close()


if __name__ == "__main__":
    game = "SuperMarioKart-Snes"
    scenario = os.path.join(code_location, "scenarios", game, "custom_rewards.json")
    # state = os.path.join(retro.data.DATA_PATH, "data", "contrib", game, "MarioCircuit1.GP.50cc.1P.Luigi.Start.state")
    # state = os.path.join(retro.data.DATA_PATH, "data", "contrib", game, "DonutPlains1.GP.50cc.1P.Koopa.Start.state")
    state = os.path.join(retro.data.DATA_PATH, "data", "contrib", game, "GhostHouse1.GP.50cc.1P.Koopa.Start.state")
    main(game, state, scenario)