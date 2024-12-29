import gym
import numpy as np

env=gym.make("drp_env:drp-2agent_map_3x3-v2", state_repre_flag = "onehot_fov")

n_obs=env.reset()
print("n_obs", n_obs, type(n_obs),)
print("action_space", env.action_space)
print("observation_space", env.observation_space)

for _ in range(50):
    env.render()

    # actions=tuple(map(int, input().split()))
    actions = tuple(np.random.randint(9) for _ in range(2))
    n_obs, reward, done, info = env.step(actions)

    print("actions", actions, "reward", reward, done)
    print("info", info)
    print("n_obs", n_obs)
