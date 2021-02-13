import retro
from retro.examples.brute import Frameskip, TimeLimit, Brute, EXPLORATION_PARAM
from utils import TetrisDiscretizer, SuperMarioKartDiscretizer, FzeroDiscretizer

# game = "Tetris-Nes"
# scenario = "C:\\Projects\\OpenAI Games\\retro-gym-hacking\\scenarios\\Tetris-Nes\\custom_rewards.json"
# state = "C:\\Users\\joncocks\\anaconda3\\envs\\retro_ai\\Lib\\site-packages\\retro\\data\\contrib\\Tetris-Nes\\Type.A.level.9.start.state"

# game = "NHLHockey94-Genesis"
# scenario = "C:\\Projects\\OpenAI Games\\retro-gym-hacking\\scenarios\\NHLHockey94-Genesis\\custom_rewards.json"
# state = "C:\\Users\\joncocks\\anaconda3\\envs\\retro_ai\\Lib\\site-packages\\retro\\data\\contrib\\NHLHockey94-Genesis\\LAK.MTL.Regular.1P.fastclock.state"

game = "SuperMarioKart-Snes"
scenario = "C:\\Projects\\OpenAI Games\\retro-gym-hacking\\scenarios\\SuperMarioKart-Snes\\custom_rewards.json"
state = "C:\\Users\\joncocks\\anaconda3\\envs\\retro_ai\\Lib\\site-packages\\retro\\data\\contrib\\SuperMarioKart-Snes\\MarioCircuit1.GP.50cc.1P.Luigi.Start.state"

# game = "Fzero-Snes"
# scenario = "C:\\Users\\joncocks\\anaconda3\\envs\\retro_ai\\Lib\\site-packages\\retro\\data\\contrib\\Fzero-Snes\\scenario.json"
# state = "C:\\Users\\joncocks\\anaconda3\\envs\\retro_ai\\Lib\\site-packages\\retro\\data\\contrib\\Fzero-Snes\\practice.mutecity.bluefalcon.norival.start.state"

max_episode_steps = 10000
timestep_limit = 1e8

env = retro.make(game, state, scenario=scenario,
                 inttype=retro.data.Integrations.CONTRIB)
if game == "Tetris-Nes":
    env = TetrisDiscretizer(env)
elif game == "SuperMarioKart-Snes":
    env = SuperMarioKartDiscretizer(env)
elif game == "Fzero-Snes":
    env = FzeroDiscretizer(env)

env = Frameskip(env)
env = TimeLimit(env, max_episode_steps=max_episode_steps)

brute = Brute(env, max_episode_steps=max_episode_steps)
timesteps = 0
best_rew = float('-inf')
while True:
    acts, rew = brute.run()
    timesteps += len(acts)

    if rew > best_rew:
        print("new best reward {} => {}".format(best_rew, rew))
        best_rew = rew
        env.unwrapped.record_movie("best.bk2")
        env.reset()
        for act in acts:
            env.step(act)
        env.unwrapped.stop_record()

    if timesteps > timestep_limit:
        print("timestep limit exceeded")
        break
