import retro
import numpy as np
import pandas
import cv2
import matplotlib.pyplot as plt
import matplotlib
import os
import shutil
from wrappers import TetrisDiscretizer

def main(game, state, scenario, video_filename=None):

    if game.endswith("-Nes"):
        sz = (224, 240, 3)
    elif game.endswith("-Genesis"):
        sz = (224, 320, 3)
    else:
        raise Exception("Unknown console: {}".format(game.split("-")[1]))

    output_folder = os.path.join('C:\\Projects\\OpenAI Games\\retro-gym-hacking\\images\\', game)
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)


    env = retro.make(game=game, state=state, scenario=scenario, inttype=retro.data.Integrations.CONTRIB)
    if game == "Tetris-Nes":
        env = TetrisDiscretizer(env)
    obs = env.reset()
    counter = 5000

    while True:
        c = 0
        imgs = []
        infos = []
        rewards = []
        timeindex = []
        while True:
            obs, rew, done, info = env.step(env.action_space.sample())
            imgs.append(env.get_screen())
            infos.append(info)
            rewards.append(rew)
            c += 1
            timeindex.append(c)
            print(c)
            if done or c > counter:
                break

        if np.any(np.array(rewards) != 0):
            env.close()
            break
        else:
            env.reset()
            print("no reward generated, retrying...")

    # Get dataframe of observations
    df = pandas.DataFrame.from_records(infos)

    # Get dimensions for plot
    px = 1 / plt.rcParams['figure.dpi']
    fig = plt.figure(figsize=(sz[1] * px, sz[0] * px))
    # Get plot image
    ax = plt.axes()
    # plot the reward observations
    plt.plot(timeindex, rewards)
    for i in range(0,len(timeindex)):
        # plot to reward tracking dot
        scatter_dot = plt.scatter(timeindex[i], rewards[i], linewidths=3, color='red', zorder=10)
        fig.canvas.draw()
        # Get the image array from the plot canvas
        plot_img = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
        plot_img = plot_img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        # Concatenate the images together
        full_img = np.concatenate((imgs[i], plot_img), axis=1)
        fn = str(i).zfill(4) + ".jpg"
        cv2.imwrite(os.path.join(output_folder, fn), full_img[:,:,(2,1,0)])
        # video_writer.write(full_img)
        scatter_dot.remove()
    # video_writer.release()

if __name__ == "__main__":
    matplotlib.rcParams['toolbar'] = 'None'
    # game = "Tetris-Nes"
    # scenario = "C:\\Projects\\OpenAI Games\\retro-gym-hacking\\scenarios\\Tetris-Nes\\custom_rewards.json"
    # state = "C:\\Users\\joncocks\\anaconda3\\envs\\retro_ai\\Lib\\site-packages\\retro\\data\\contrib\\Tetris-Nes\\Type.A.level.0.mid.state"
    game = "NHLHockey94-Genesis"
    scenario = "C:\\Projects\\OpenAI Games\\retro-gym-hacking\\scenarios\\NHLHockey94-Genesis\\custom_rewards.json"
    state = "C:\\Users\\joncocks\\anaconda3\\envs\\retro_ai\\Lib\\site-packages\\retro\\data\\contrib\\NHLHockey94-Genesis\\LAK.MTL.Regular.1P.fastclock.state"
    main(game, state, scenario, video_filename="C:\\Projects\\OpenAI Games\\retro-gym-hacking\\" + game + ".avi")