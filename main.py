from retro.scripts import playback_movie
from retro.examples import brute
from retro import RetroEnv
import pandas
import retro
from baselines.common.retro_wrappers import make_retro
from utils import TetrisDiscretizer

game = "Tetris-Nes"
state = "C:\\Users\\joncocks\\anaconda3\\envs\\retro_ai\\Lib\\site-packages\\retro\\data\\contrib\\Tetris-Nes\\Type.A.level.0.mid.state"
scenario = "C:\\Projects\\OpenAI Games\\retro-gym-hacking\\scenarios\\custom_rewards.json"

n_sims = 20
n = 1
env = make_retro(game=game,
                 state=state,
                 scenario=scenario,
                 inttype=retro.data.Integrations.CONTRIB)
env = TetrisDiscretizer(env)
# rews = []
# infos = []
# sim_number = []
# sim_step = []
# while n <= n_sims:
#     stepcount = 0
#     env.reset()
#     while True:
#         _obs, _rew, done, _info = env.step(env.action_space.sample())
#         stepcount += 1
#         sim_step.append(stepcount)
#         rews.append(_rew)
#         infos.append(_info)
#         sim_number.append(n)
#         if done:
#             print("Sim number {} complete".format(n))
#             n += 1
#             break
# data = pandas.DataFrame.from_records(infos)
# data["reward"] = rews
# data["sim_number"] = sim_number
# data["sim_stepcount"] = sim_step
# print("Simulation complete")
# data.to_csv("test.csv")


env.reset()
brute.brute_retro(env)



# movie_name = "C:\\Projects\\OpenAI Games\\retro-gym-hacking\\foo.bk2"
# env = retro.make(game='Tetris-Nes',
#                  inttype=retro.data.Integrations.CONTRIB, record=movie_name, state=retro.State.DEFAULT)
# obs = env.reset()
#
# while True:
#     _obs, _rew, done, _info = env.step(env.action_space.sample())
#     if done:
#         break

