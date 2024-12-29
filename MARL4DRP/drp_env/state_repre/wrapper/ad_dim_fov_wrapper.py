import numpy as np
import networkx as nx

def ad_dim_fov_obs(env, state_repre_flag):
    agent_num = env.agent_num
    n_act = env.n_actions
    all_onehot_obs = np.array(env.obs_onehot)
    onehot_obs = all_onehot_obs[:, :n_act] #スライシング処理
    G = env.ee_env.G
    
    state = [0] * n_act
    pos_list = []
    
    # get all agent state and position
    for i, obs_i in enumerate(onehot_obs):
        edge_or_node = tuple([i for i, o in enumerate(obs_i) if o!=0])
        if len(edge_or_node)==1:
            node = edge_or_node[0]
            pos = {"type": "n", "pos": node}
            obs_i = np.array(obs_i)*agent_num
        else:
            edge = edge_or_node
            pos = {"type": "e", "pos": edge, "current_goal": env.current_goal[i], "current_start": env.current_start[i], "obs": obs_i}
        state += obs_i
        pos_list.append(pos)
    print("state", state)
    print("pos_list", pos_list)
    
    
    if state_repre_flag=="small_onehot_fov":
        small_fov_onehot = calc_small_fov(pos_list, G, state, n_act, agent_num) #return np.array
        all_small_fov_obs = np.hstack((all_onehot_obs, small_fov_onehot))
        print(f'all_small_fov_obs = {all_small_fov_obs}')
        return all_small_fov_obs
    elif state_repre_flag=="medium_onehot_fov":
        medium_fov_onehot = calc_medium_fov(pos_list, G, state, n_act, agent_num)
        all_medium_fov_obs = np.hstack((all_onehot_obs, medium_fov_onehot))
        print(f'all_medium_fov_obs = {all_medium_fov_obs}')
        return all_medium_fov_obs
    elif state_repre_flag=="large_onehot_fov":
        large_fov_onehot = calc_large_fov(pos_list, G, state, n_act, agent_num)
        all_large_fov_obs = np.hstack((all_onehot_obs, large_fov_onehot))
        print(f'all_large_fov_obs = {all_large_fov_obs}')
        return all_large_fov_obs
    
    
def get_edge_agent_curent_start_current_goal(agent_pos):
    assert agent_pos['type'] == 'e', 'agent_pos["type"] must be "e"'
    return agent_pos['current_start'], agent_pos['current_goal']
    
def get_nodes_to_be_consideration(agent_pos, graph):
    """
    start_node, target_nodeのtypeは配列で統一
    """
    if agent_pos['type']=='n':
        start_node = list()
        start_node.append(agent_pos['pos'])
        target_node = list(nx.neighbors(graph, start_node[0]))
        # print(f'########## node : current_goal = {list(nx.neighbors(graph, start_node[0]))}#########')
    elif agent_pos['type']=='e':
        start_node = list()
        start_node.append(agent_pos['current_start'])
        target_node = list()
        target_node.append(agent_pos['current_goal'])
        # print(f' edge : current_goal = {agent_pos["current_goal"]}')
    # print(f'in get_nodes_to : start_node = {start_node}, target_node = {target_node}')
    return start_node, target_node

def calc_small_fov(pos_list, graph, state, n_act, agent_num):
    agents_fov_list = list()
    for i in range(agent_num):
        agent_fov_list = np.zeros(n_act)
        start_node, target_node = get_nodes_to_be_consideration(pos_list[i], graph)
        if pos_list[i]['type']=='n': #エージェントがノードにいる場合
            for age in range(agent_num):
                if age!=i and pos_list[age]['type']=='n' and pos_list[age]['pos'] in target_node:
                    agent_fov_list[pos_list[age]['pos']] += -1 #隣接ノードにエージェントがいる場合-1
                elif age!=i and pos_list[age]['type']=='e' and pos_list[age]['current_goal']==start_node[0]:
                    danger_agent_start, danger_agent_goal = get_edge_agent_curent_start_current_goal(pos_list[age])
                    danger_agent_pos = pos_list[age]['obs']
                    #加算
                    agent_fov_list[danger_agent_start] += -danger_agent_pos[danger_agent_start]
                    agent_fov_list[danger_agent_goal] += -1
        elif pos_list[i]['type']=='e':
            for age in range(agent_num):
                if age!=i and pos_list[age]['type']=='n' and pos_list[age]['pos']==target_node[0]:
                    agent_fov_list[pos_list[age]['pos']] += -1
                elif age!=i and pos_list[age]['type']=='e' and pos_list[age]['current_goal']==target_node[0]:
                    danger_agent_start, danger_agent_goal = get_edge_agent_curent_start_current_goal(pos_list[age])
                    danger_agent_pos = pos_list[age]['obs']
                    #加算
                    agent_fov_list[danger_agent_start] += -danger_agent_pos[danger_agent_start]
                    agent_fov_list[danger_agent_goal] += -1
        agents_fov_list.append(agent_fov_list)
    return np.array(agents_fov_list)

def calc_medium_fov(pos_list, graph, state, n_act, agent_num):
    agents_fov_list = list()
    for i in range(agent_num):
        agent_fov_list = np.zeros(n_act)
        start_node, target_node = get_nodes_to_be_consideration(pos_list[i], graph)
        all_target_node = target_node + start_node
        if pos_list[i]['type']=='n': #エージェントがノードにいる場合
            print(f'start_node = {start_node}, target_node = {target_node}, all_target_node = {all_target_node}')
            for age in range(agent_num):
                if age!=i and pos_list[age]['type']=='n' and pos_list[age]['pos'] in target_node:
                    agent_fov_list[pos_list[age]['pos']] += -1
                elif age!=i and pos_list[age]['type']=='e' and pos_list[age]['current_goal'] in all_target_node:
                    danger_agent_start, danger_agent_goal = get_edge_agent_curent_start_current_goal(pos_list[age])
                    danger_agent_pos = pos_list[age]['obs']
                    #加算
                    agent_fov_list[danger_agent_start] += -danger_agent_pos[danger_agent_start]
                    agent_fov_list[danger_agent_goal] += -1
        elif pos_list[i]['type']=='e':
            adjacent_node = list(nx.neighbors(graph, target_node[0]))
            adjacent_node_plus_target_node = adjacent_node + target_node
            all_target_node = [item for item in adjacent_node_plus_target_node if item not in start_node]
            print(f'start_node = {start_node}, target_node = {target_node}, all_target_node = {all_target_node}')
            for age in range(agent_num):
                if age!=i and pos_list[age]['type']=='n' and pos_list[age]['pos'] in all_target_node:
                    agent_fov_list[pos_list[age]['pos']] += -1
                elif age!=i and pos_list[age]['type']=='e' and pos_list[age]['current_goal'] in all_target_node:
                    danger_agent_start, danger_agent_goal = get_edge_agent_curent_start_current_goal(pos_list[age])
                    danger_agent_pos = pos_list[age]['obs']
                    #加算
                    agent_fov_list[danger_agent_start] += -danger_agent_pos[danger_agent_start]
                    agent_fov_list[danger_agent_goal] += -1
        agents_fov_list.append(agent_fov_list)
    return np.array(agents_fov_list)
                        
def calc_large_fov(pos_list, graph, state, n_act, agent_num):
    agents_fov_list = list()
    for i in range(agent_num):
        agent_fov_list = np.zeros(n_act)
        for age in range(agent_num):
            if age!=i and pos_list[age]['type']=='n':
                agent_fov_list[pos_list[age]['pos']] += -1
            elif age!=i and pos_list[age]['type']=='e':
                danger_agent_start, danger_agent_goal = get_edge_agent_curent_start_current_goal(pos_list[age])
                danger_agent_pos = pos_list[age]['obs']
                #加算
                agent_fov_list[danger_agent_start] += -danger_agent_pos[danger_agent_start]
                agent_fov_list[danger_agent_goal] += -1
        agents_fov_list.append(agent_fov_list)
    return np.array(agents_fov_list)