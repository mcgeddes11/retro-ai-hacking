import retro
from wrappers import TetrisDiscretizer, SuperMarioKartDiscretizer, SuperMarioKartObservationWrapper, RewardScaler, SuperMarioKartRewardWrapper
from stable_baselines3.common.atari_wrappers import WarpFrame
from environments import SuperMarioKartEnv
from matplotlib import pyplot as plt
from retro.examples.brute import Frameskip, TimeLimit, Brute
from stable_baselines3.common.monitor import Monitor


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
    # game = "Tetris-Nes"
    # scenario = "C:\\Projects\\OpenAI Games\\retro-ai-hacking\\scenarios\\Tetris-Nes\\custom_rewards.json"
    # state = "C:\\Users\\joncocks\\anaconda3\\envs\\retro_ai_3\\Lib\\site-packages\\retro\\data\\contrib\\Tetris-Nes\\Type.A.level.0.mid.state"
    # game = "NHLHockey94-Genesis"
    # scenario = "C:\\Projects\\OpenAI Games\\retro-ai-hacking\\scenarios\\NHLHockey94-Genesis\\custom_rewards.json"
    # state = "C:\\Users\\joncocks\\anaconda3\\envs\\retro_ai_3\\Lib\\site-packages\\retro\\data\\contrib\\NHLHockey94-Genesis\\LAK.MTL.Regular.1P.fastclock.state"
    game = "SuperMarioKart-Snes"
    scenario = "C:\\Projects\\OpenAI Games\\retro-ai-hacking\\scenarios\\SuperMarioKart-Snes\\custom_rewards.json"
    # state = "C:\\Users\\joncocks\\anaconda3\\envs\\retro_ai_3\\Lib\\site-packages\\retro\\data\\contrib\\SuperMarioKart-Snes\\DonutPlains1.GP.50cc.1P.Koopa.Start"
    state = "C:\\Users\\joncocks\\anaconda3\\envs\\retro_ai_3\\Lib\\site-packages\\retro\\data\\contrib\\SuperMarioKart-Snes\\MarioCircuit1.GP.50cc.1P.Luigi.Start.state"
    main(game, state, scenario)