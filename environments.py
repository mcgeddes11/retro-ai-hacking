from retro import RetroEnv
import retro
import numpy as np
import gym
import math
from scipy.ndimage import rotate
from matplotlib import pyplot as plt
import cv2
from utils import rotate_image

class SuperMarioKartEnv(RetroEnv):

    def __init__(self, game, state=retro.State.DEFAULT, scenario=None, sprite_buffer=20,
                 **kwargs):
        RetroEnv.__init__(self, game, state, scenario, **kwargs)
        self.map = None
        self.sprite_buffer = sprite_buffer # defines visual area around kart; values 5-50 probably fine

        # colormap for physics representation on overhead map
        self.colormap = {"road": [175,175,175],
                         "slowroad": [210,210,210],
                         "offroad": [255,255,255],
                         "outofbounds": [0,0,0],
                         "coins": [255,255,0],
                         "playerkart": [255,0,0],
                         "enemykart": [0,0,255]}


    def get_screen(self, player=0):
        # Check the game mode
        game_mode_var = self.data.get_variable("game_mode")
        game_mode = self.data.memory.extract(game_mode_var["address"], game_mode_var["type"])

        # Get kart direction
        direction = self.data.memory.extract(int("0x95", 16), "|u1")

        # adjust the direction
        direction = (direction / 255) * 360

        if game_mode != 28:
            # return np.zeros((32, 32, 3)).astype("uint8")
            return np.zeros((128, 128, 3)).astype("uint8")
        # If we're in gameplay
        else:
            # Update the base map layer if necessary
            if self.map is None:
                self.map = self.read_map().astype("uint8")
            # Make a copy and update the map with player position
            this_map = np.copy(self.map)
            # Get scaled player position on map
            player_position_east = self.data.memory.extract(8257672, "<u2")
            player_position_south = self.data.memory.extract(8257676, "<u2")
            player_position_east_relative = math.floor((player_position_east / 4100) * 128)
            player_position_south_relative = math.floor((player_position_south / 4100) * 128)

            # Update the player position to be red
            this_map[player_position_south_relative, player_position_east_relative, :] = self.colormap["playerkart"]

            # add enemy karts
            positions = self.get_cpu_kart_pos()
            for player_num, position_dict in positions.items():
                if position_dict["east"] == player_position_east and position_dict["south"] == player_position_south:
                    continue
                else:
                    p_south_rel = math.floor(((position_dict["south"] / 4100.0) * 128))
                    p_east_rel = math.floor(((position_dict["east"] / 4100.0) * 128))
                    this_map[p_south_rel, p_east_rel,:] = self.colormap["enemykart"]

            # Pad using sprite buffer
            # Original image generated from RAM is 128x128
            a = np.concatenate((np.zeros((128, self.sprite_buffer, 3)), this_map), axis=1)
            a = np.concatenate((a, np.zeros((128, self.sprite_buffer, 3))), axis=1)
            a = np.concatenate((a, np.zeros((self.sprite_buffer, 128+self.sprite_buffer*2, 3))), axis=0)
            a = np.concatenate((np.zeros((self.sprite_buffer, 128+self.sprite_buffer*2, 3)), a), axis=0)

            # Now need to account for padding
            smallmap = a[player_position_south_relative:player_position_south_relative + self.sprite_buffer*2,
                   player_position_east_relative:player_position_east_relative+self.sprite_buffer*2, :]
            # Rotate
            smallmap = rotate_image(smallmap, direction).astype("uint8")
            # Scale back to 128x128 dimensions CNN can handle
            dim = (128, 128)
            smallbigmap = cv2.resize(smallmap, dim, interpolation=cv2.INTER_AREA)
            return smallbigmap




    def read_map(self):
        # This base tile contains the first spritemap byte.
        # We read them all into a 128x128 matrix to represent the overhead map
        base_tile_address = 8323072
        base_physics_address = int("0xB00", 16)
        map = np.empty(shape=(128,128), dtype="object")
        for x in range(1,129):
            for y in range(1,129):
                address = base_tile_address+((x-1)+(y-1)*128)*1
                tile = self.data.memory.extract(address, "|u1")
                # extract physics elements of each tile
                physics = self.get_generalizable_physics(self.data.memory.extract(base_physics_address+tile, "|u1"))
                map[x-1, y-1] = physics
        map = np.fliplr(map)
        map = np.rot90(map)
        map = self.get_map_from_physics_array(map)
        return map

    def get_map_from_physics_array(self, physics_array):
        map_image = np.zeros((128,128,3))
        for row in range(0,128):
            for col in range(0,128):
                map_image[row,col,:] = self.colormap[physics_array[row,col]]
        return map_image

    def get_cpu_kart_pos(self):
        pos = {}
        for k in range(2,9):
            base = int("0xF00", 16) + int("0x100", 16) * k
            x = self.data.memory.extract(int("0x18", 16) + base, "<2") * 4
            y = self.data.memory.extract(int("0x1C", 16) + base, "<2") * 4
            pos[k] = {"east": x, "south": y}
        return pos


    def render(self, mode='human', close=False):
        # Mimics functionality of parent render method, but adds lowres overlay
        if close:
            if self.viewer:
                self.viewer.close()
            return
        # Get game and overlay screens
        game_img = RetroEnv.get_screen(self)
        game_img_shape = game_img.shape
        lowres_overhead = self.get_screen()
        lowres_shape = lowres_overhead.shape
        # Extend the image
        actual_game_image = np.concatenate((game_img,np.zeros((game_img_shape[0], lowres_shape[1], 3))), axis=1)
        actual_game_image[0:lowres_shape[0],
                          game_img_shape[1]:game_img_shape[1] + lowres_shape[1],
                          :] = lowres_overhead
        actual_game_image = actual_game_image.astype("uint8")

        # Scale
        scale_percent = 400
        width = int(actual_game_image.shape[1] * scale_percent / 100)
        height = int(actual_game_image.shape[0] * scale_percent / 100)
        dim = (width, height)

        # resize image
        actual_game_image = cv2.resize(actual_game_image, dim, interpolation=cv2.INTER_AREA)


        if mode == "rgb_array":
            return actual_game_image
        elif mode == "human":
            if self.viewer is None:
                from gym.envs.classic_control.rendering import SimpleImageViewer
                self.viewer = SimpleImageViewer(maxwidth=width)
            self.viewer.imshow(actual_game_image)
            return self.viewer.isopen

    def get_generalizable_physics(self, physics):

        # Map the following to "road":
        # road, dirt road, ghost road, light ghost road, wood bridge, starting line, castle road, speed boost, jump pad,
        # choco road, sand road, ? box, coins
        #

        if physics == int("0x40", 16): # road
            return "road"
        elif physics == int("0x46",16): # --dirt road
            return "road"
        elif physics == int("0x42",16): # --ghost road
            return "road"
        elif physics == int("0x4E",16): # --light ghost road
            return "road"
        elif physics == int("0x50",16): # --wood bridge
            return "road"
        elif physics == int("0x1E",16): # --starting line
            return "road"
        elif physics == int("0x44",16): # --castle road
            return "road"
        elif physics == int("0x16",16): # --speed boost
            return "road"
        elif physics == int("0x10",16): # --jump pad
            return "road"
        elif physics == int("0x4C",16): # --choco road
            return "road"
        elif physics == int("0x4A",16): # --sand road
            return "road"
        elif physics == int("0x14",16): # --? box
            return "road"
        elif physics == int("0x54",16): # --dirt
            return "offroad"
        elif physics == int("0x5A",16): # --lily pads/grass
            return "offroad"
        elif physics == int("0x5C",16): # --shallow water
            return "offroad"
        elif physics == int("0x58",16): # --snow
            return "offroad"
        elif physics == int("0x1A",16): # --coin
            return "road"
        elif physics == int("0x52",16): # --loose dirt
            return "slowroad"
        elif physics == int("0x5E",16): # --mud
            return "slowroad"
        elif physics == int("0x48",16): # --wet sand
            return "slowroad"
        elif physics == int("0x12",16): # --choco bump
            return "slowroad"
        elif physics == int("0x1C",16): # --choco bump
            return "slowroad"
        elif physics == int("0x18",16): # --oil spill
            return "slowroad"
        elif physics == int("0x80",16): # --wall
            return "outofbounds"
        elif physics == int("0x26",16): # --oob grass
            return "outofbounds"
        elif physics == int("0x22",16): # --deep water
            return "outofbounds"
        elif physics == int("0x20",16): # --pit
            return "outofbounds"
        elif physics == int("0x82",16): # --ghost house border
            return "outofbounds"
        elif physics == int("0x24",16): # --lava
            return "outofbounds"
        elif physics == int("0x84",16): # --ice blocks
            return "outofbounds"
        else:
            return "offroad"

    def get_physics(self, physics):
        if physics == int("0x54",16): # --dirt
            return 0
        elif physics == int("0x5A",16): # --lily pads/grass
            return 0
        elif physics == int("0x5C",16): # --shallow water
            return 0
        elif physics == int("0x58",16): # --snow
            return 0
        elif physics == int("0x56",16): # --chocodirt
            return -0.5
        elif physics == int("0x40",16): # --road
            return 1
        elif physics == int("0x46",16): # --dirt road
            return 0.75
        elif physics == int("0x52",16): # --loose dirt
            return 0.5
        elif physics == int("0x42",16): # --ghost road
            return 1
        elif physics == int("0x10",16): # --jump pad
            return 1.5
        elif physics == int("0x4E",16): # --light ghost road
            return 1
        elif physics == int("0x50",16): # --wood bridge
            return 1
        elif physics == int("0x1E",16): # --starting line
            return 1
        elif physics == int("0x44",16): # --castle road
            return 1
        elif physics == int("0x16",16): # --speed boost
            return 2
        elif physics == int("0x80",16): # --wall
            return -1.5
        elif physics == int("0x26",16): #	--oob grass
            return -1.5
        elif physics == int("0x22",16): # --deep water
            return -1
        elif physics == int("0x20",16): # --pit
            return -2
        elif physics == int("0x82",16): # --ghost house border
            return -1.5
        elif physics == int("0x24",16): # --lava
            return -2
        elif physics == int("0x4C",16): # --choco road
            return 1
        elif physics == int("0x12",16): # --choco bump
            return 0.75
        elif physics == int("0x1C",16): # --choco bump
            return 0.75
        elif physics == int("0x5E",16): # --mud
            return 0.5
        elif physics == int("0x48",16): # --wet sand
            return 0.75
        elif physics == int("0x4A",16): # --sand road
            return 1
        elif physics == int("0x84",16): # --ice blocks
            return -1.5
        elif physics == int("0x28",16): # --unsure
            return -1
        elif physics == int("0x14",16): # --? box
            return 1.5
        elif physics == int("0x1A",16): # --coin
            return 1.25
        elif physics == int("0x18",16): # --oil spill
            return -0.75
        else:
            raise(Exception("Unknown physics: {}".format(physics)))


