"""
Reinforcement learning maze example.

Red rectangle:          explorer.
Black rectangles:       hells       [reward = -1].
Yellow bin circle:      paradise    [reward = +1].
All other states:       ground      [reward = 0].

This script is the main part which controls the update method of this example.
The RL is in RL_brain.py.

View more on my tutorial page: https://morvanzhou.github.io/tutorials/
"""
from RL_brain import QLearningTable
from Services_nums import cal_num
import time


# 超参数配置
nodeSet_file = "test/90/5/nodeSet.txt"
conf_file = "test/90/5/conf.xml"
outfile = "save/qlearning_90_5_3.txt"
ALPHA = 0.2  # learning rate
GAMMA = 0.9    # reward_decay
EPSILON = 0.60  # e_greedy
MAX_EPISODES = 300000  # 最大迭代轮数
ERROR_COUNT = 100   # 连续100次，reward变化在误差允许范围内，则提前终止实验
ERROR_RANGE = 0.0001   # 误差范围
judge_list = []


def update():
    start = time.time()
    RL = QLearningTable(n_states=nodes_num, each_services_nums=each_services_nums,
                        max_services_num=max_services_num,
                        nodeSet_file=nodeSet_file, conf_file=conf_file,
                        learning_rate=ALPHA, reward_decay=GAMMA, e_greedy=EPSILON)
    max_reward = 0

    for episode in range(MAX_EPISODES):
        # initial observation
        state = 0
        # print("episode = {}".format(episode))

        while True:
            # RL choose action based on observation
            action = RL.choose_action(state)

            # RL take action and get next observation and reward
            state_, reward, done = RL.step(state, action)

            # print("s = {0}, a = {1}, s_ = {2}, reward = {3}".format(
            #     state, action, state_, reward
            # ))

            # RL learn from this transition
            RL.learn(state, action, reward, state_)

            # swap observation
            state = state_

            # break while loop when end of this episode
            if done:
                # print("services = {0}, reward = {1}, runtime = {2}, episode = {3} ".format
                #       (RL.choose_services, reward, time.time()-start, episode))
                if episode == 0:
                    max_reward = reward
                else:
                    if reward > max_reward:
                        max_reward = reward
                        print("services = {0}, reward = {1}, runtime = {2}, episode = {3} ".format
                              (RL.choose_services, reward, time.time() - start, episode))
                        line = [x for x in RL.choose_services]
                        line.append(reward)
                        line.append(time.time() - start)
                        line.append(episode)
                        # print(line)
                        fp = open(outfile, 'a+')
                        fp.write(str(line) + '\n')
                        fp.close()
                    else:
                        if episode % 100 == 0:
                            print("episode = {}".format(episode))
                break

        # 终止条件
        if episode >= ERROR_COUNT:
            del judge_list[0]
        judge_list.append(reward)

        if episode >= 1000 and episode % ERROR_COUNT == 0:
            if max(judge_list) - min(judge_list) <= ERROR_RANGE:
                output = "\n  达到收敛条件，提前终止实验！\n"
                line = [x for x in RL.choose_services]
                line.append(reward)
                line.append(time.time() - start)
                line.append(episode)
                # 打印收敛结果
                print(output)
                print(line)
                # 记录收敛结果
                fp = open(outfile, 'a+')
                fp.write(output)
                fp.write(str(line) + '\n')
                fp.close()
                break

    print('game over')


if __name__ == "__main__":

    nodes_num, each_services_nums, all_services_nums, max_services_num = cal_num(nodeSet_file)
    print("1.服务节点数：{}".format(nodes_num))
    print("2.每个节点处候选子集大小：{}".format(each_services_nums))
    print("3.总的候选原子个数：{}".format(all_services_nums))
    print("4.最大候选子集个数：{}".format(max_services_num))

    update()
