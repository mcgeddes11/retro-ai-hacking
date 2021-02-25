import retro
from train_ppo_refactor import get_env
import numpy

game = "SuperMarioKart-Snes"
scenario = "C:\\Projects\\OpenAI Games\\retro-ai-hacking\\scenarios\\SuperMarioKart-Snes\\custom_rewards.json"
state = "C:\\Users\\joncocks\\anaconda3\\envs\\retro_ai\\Lib\\site-packages\\retro\\data\\contrib\\SuperMarioKart-Snes\\MarioCircuit1.GP.50cc.1P.Luigi.Start.state"

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

