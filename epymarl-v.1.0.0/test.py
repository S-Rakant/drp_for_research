import numpy as np
import random


n_actions = 9
agent_num = 3
joint_action = [4, 7, 5]
adj = [[0, 3, 4, 6], [1, 3, 4, 5, 7], [4]]
pos_list = [{'type': 'n', 'pos': 3}, {'type': 'n', 'pos': 4}, {'type': 'e', 'pos': (4, 1)}]


def step(joint_action):
    print(f'step')
    print(f'joint_action = {joint_action}')
    #pos_list = [{'type': 'n', 'pos': 3}, {'type': 'n', 'pos': 4}, {'type': 'e', 'pos': (1, 4), 'current_goal': 4, 'current_start': 1, 'obs': array([0.  , 0.79, 0.  , 0.  , 0.21, 0.  , 0.  , 0.  , 0.  ])}]
    copy_joint_action = joint_action
    edge_agent_pos = [(i, pos['pos']) for i, pos in enumerate(pos_list) if pos['type']=='e']
    node_agent_action = {age: action for age, action in enumerate(copy_joint_action) if pos_list[age]['type']=='n'}
    print(f'node_agent_action = {node_agent_action}')
    print(f'edge_agent_pos = {edge_agent_pos}')
    for age in range(agent_num):
        adjacent_node = adj[age]
        print(f'adjacent = {adjacent_node}')
        bad_action = set()
        restrict = False
        if pos_list[age]['type']=='n':
            for other_agent in range(agent_num):
                # print(f'pos_list[other_agent][pos]_type = {type(pos_list[other_agent]["pos"])}')
                if other_agent!=age and pos_list[other_agent]['type']=='n' and pos_list[other_agent]['pos'] in adjacent_node and node_agent_action[other_agent]==pos_list[age]['pos']:
                    bad_action.add(pos_list[other_agent]['pos'])
                    if node_agent_action[age]==pos_list[other_agent]['pos']:
                        restrict = True
                elif other_agent!=age and pos_list[other_agent]['type']=='e':
                    age_tuple = (pos_list[age]['pos'], node_agent_action[age])
                    other_agent_tuple = pos_list[other_agent]['pos']
                    reversed_other_agent_tuple = other_agent_tuple[::-1]
                    if age_tuple==other_agent_tuple or age_tuple==reversed_other_agent_tuple:
                        bad_action.add(pos_list[other_agent]['pos'][1] if pos_list[other_agent]['pos'][1]!=pos_list[age]['pos'] else pos_list[other_agent]['pos'][0])
                        restrict = True
        if restrict:
            print(f'agent{age}のactionが制約によって変更されました.')
            print(f'bad_action = {bad_action}')
            candidate = [int(item) for item in np.arange(n_actions) if item not in bad_action]
            node_agent_action[age] = random.choice(candidate)
            copy_joint_action[age] = node_agent_action[age]
    joint_action = copy_joint_action
    print(f'joint_action = {joint_action}')
    
step(joint_action)

