import os
import retro
from stable_baselines.common.cmd_util import make_atari_env
from utils import TetrisDiscretizer
from stable_baselines import PPO2
from stable_baselines.common.policies import MlpPolicy, MlpLstmPolicy, CnnPolicy, CnnLstmPolicy
from stable_baselines.common.evaluation import evaluate_policy
from stable_baselines.common.vec_env import DummyVecEnv, VecNormalize


# Define inputs
game = "Tetris-Nes"
state = retro.State.DEFAULT
scenario = "C:\\Projects\\OpenAI Games\\retro-gym-hacking\\scenarios\\custom_rewards.json"

# Create environment
env = retro.make(game=game,
                 state=state,
                 scenario=scenario,
                 inttype=retro.data.Integrations.CONTRIB)
env = TetrisDiscretizer(env)
env = DummyVecEnv([lambda: env])
env = VecNormalize(env, norm_obs=True, norm_reward=True,
                   clip_obs=10.)
env.reset()

# Instantiate the agent
# if os.path.exists("cnn_tetris"):
#     # Load the trained agent
#     model = PPO2.load("cnn_tetris")
# else:
model = PPO2('CnnPolicy', env, learning_rate=1e-3, verbose=1)

# Train the agent
model.learn(total_timesteps=int(1000))
# Save the agent
model.save("cnn_tetris")

# Evaluate the agent
mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10)
print("Mean Reward: {}\nStd Reward: {}\n".format(mean_reward, std_reward))

# # Enjoy trained agent
# obs = env.reset()
# for i in range(1000):
#     action, _states = model.predict(obs)
#     obs, rewards, dones, info = env.step(action)
#     env.render()