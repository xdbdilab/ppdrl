"""
This part of code is the Q learning brain, which is a brain of the agent.
All decisions are made in here.

View more on my tutorial page: https://morvanzhou.github.io/tutorials/
"""

import numpy as np
import pandas as pd
from calattr import *


class QLearningTable:
    def __init__(self, n_states, each_services_nums, max_services_num, nodeSet_file, conf_file,
                 learning_rate, reward_decay, e_greedy, e_greedy_increment=0.01):
        self.each_services_nums = each_services_nums
        self.n_actions = max_services_num
        self.n_states = n_states
        self.nodeSet_file = nodeSet_file
        self.conf_file = conf_file
        self.lr = learning_rate
        self.gamma = reward_decay
        self.choose_services = [0 for i in range(self.n_states)]

        # self.epsilon = e_greedy
        self.epsilon_max = e_greedy  # 90%的可能选择Q估计最大的行为
        self.epsilon_increment = e_greedy_increment  # 不断的缩小随机范围
        self.epsilon = 0 if e_greedy_increment is not None else self.epsilon_max

        services_tmp_list = [[0]*self.each_services_nums[i] for i in range(len(each_services_nums))]

        # self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)
        # 无效部分是：NAN
        self.q_table = pd.DataFrame(
            services_tmp_list,  # q_table initial values
            columns=list(range(self.n_actions)))  # actions's name(原子服务)

    def choose_action(self, state):
        # action selection
        state_action = self.q_table.loc[state, :self.each_services_nums[state]]  # （有效区域）
        # if np.random.uniform() < self.epsilon:
        if (np.random.uniform() > self.epsilon) or ((state_action == 0).all()):
            # choose random action
            action = np.random.choice(list(range(self.each_services_nums[state])))
        else:
            # choose best action
            # some actions may have the same value, randomly choose on in these actions
            action = np.random.choice(state_action[state_action == np.max(state_action)].index)
        self.choose_services[state] = action
        return action

    def learn(self, s, a, r, s_):
        q_predict = self.q_table.loc[s, a]
        if s_ != -1:
            q_target = r + self.gamma * self.q_table.loc[s_, :self.each_services_nums[s_]].max()  # next state is not terminal
        else:
            q_target = r  # next state is terminal
        self.q_table.loc[s, a] += self.lr * (q_target - q_predict)  # update

        # 逐渐增加 epsilon, 降低行为的随机性
        self.epsilon = self.epsilon + self.epsilon_increment if self.epsilon < self.epsilon_max else self.epsilon_max

    # state_, reward, done
    def step(self, s, a):
        if s == self.n_states - 1:
            done = True
            s_ = -1
            # 计算Qos值
            calattr = Calattr(self.conf_file, self.nodeSet_file)
            f = calattr.receive(self.choose_services)
            reward = f
        else:
            done = False
            s_ = s + 1
            reward = 0

        return s_, reward, done




"""
1.action此处选择的是:最大的子集（109）,但是并不是每个状态下都是109个选择，需要引入each_services_nums
  选取有效区域，（不能影响max的选择）
2.参考一维案例: -----T
3.state表示的是每个节点，nodeset有多少个节点就有多少个state.
  并且：s' = s + 1 (固定)
  每轮实验：依次选择每个state对应的action(原子服务)，中间过程 reward = 0
  在每轮实验结束时：添加reward（Qos）的计算值（reward = Qos）
4.设置超参数
"""
