import gym.spaces
import numpy as np
import gym

from drp_env.state_repre.wrapper.ad_dim_fov_wrapper import ad_dim_fov_obs

class AdDimOnehotSmallFov:
    def __init__(self, env) -> None:
        self.env = env
    
    def get_obs_box(self):
        n_nodes = len(self.env.G.nodes)
        obs_box = gym.spaces.Box(np.zeros(n_nodes*3), np.array([100]*(n_nodes*3)))
        return obs_box
    
    def calc_obs(self):
        return ad_dim_fov_obs(self.env, "small_onehot_fov")