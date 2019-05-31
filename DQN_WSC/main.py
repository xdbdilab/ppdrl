import tensorflow as tf
from Qnetwork import Qnetwork
from optimizer import Optimize
from sc_dataset import SC_DataGenerator
from config import get_config
from calattr import Calattr
import numpy as np
import datetime
from tqdm import tqdm
config, _ = get_config()
f_path=config.train_from+'//nodeSet.txt'
data_set = SC_DataGenerator()
data_set.init(f_path)
MEMORY = np.zeros([config.memory_capacity,4])     # [s,a,r,s+1]
num_service=data_set.num_service
max_action_num=np.max(num_service)

def main():
    epsilon = config.min_epsilon
    state = tf.placeholder(tf.float32, [1],name="state")
    reward=tf.placeholder(tf.float32,name="reward")
    next_state=tf.placeholder(tf.float32, [1],name="next_state")
    action = tf.placeholder(tf.int32, name="action")

    global_step = tf.Variable(0, trainable=False, name="global_step")

    q_network = Qnetwork(config,scope="q",max_action_num=max_action_num)
    target_q_network=Qnetwork(config,scope="target_q",max_action_num=max_action_num)
    optimize = Optimize(config, global_step)


    #max_a = q_network.choose_action(state=state,cur_max_action_num=action_num)
    Q_score=q_network.get_q_score(state=state,a=action)
    Q_scores = q_network.get_q_scores(state)

    #target_max_a=target_q_network.choose_action(state=next_state,cur_max_action_num=action_num)
    target_Q_score=target_q_network.get_q_score(state=next_state,a=action)
    target_Q_scores = target_q_network.get_q_scores(next_state)

    optimize.build_optim(reward, Q_score)

    with tf.Session() as sess:
        starttime = datetime.datetime.now()
        sess.run(tf.global_variables_initializer())
        sess.run(tf.local_variables_initializer())
        #使targe q网络的参数等与q网络的参数
        t_params = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='target_q')
        e_params = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='q')
        sess.run([tf.assign(t, e) for t, e in zip(t_params, e_params)])

        device = '/cpu:0'
        with tf.device(device):
            print("begin training....")
            training_step=0  #记录获得过多少次[s,a,r,s+1]
            max_qos = -10000
            for k in tqdm(range(config.nb_epoch)):#总的大循环
                #print('train step '+str(k+1))
                conf_dir=config.train_from+'//conf.xml'
                calattr = Calattr()
                calattr.init(conf_dir,config.train_from)
                s=0 #当前状态
                position=[] #记录整个内循环选择出的各个服务，用于计算组合服务qos值
                for t in range(config.node_num):
                    #根据epsilon贪婪选择出当前状态的动作
                    if np.random.uniform() < epsilon:
                        q_scores=sess.run(Q_scores,feed_dict={state:[s]})[0: num_service[s]]
                        a_choosen=np.argmax(q_scores)
                    else:
                        a_choosen = np.random.randint(0, num_service[s])
                    position.append(a_choosen)

                    # 得到[s,a,r,s+1]，并存储进memory里（容量1000）
                    if(s == (config.node_num-1)):#如果s已经是最后一个抽象原子服务了，r=qos
                        r_d=calattr.receive(position)#qos
                        print(r_d)
                        if(r_d>max_qos):
                            max_qos=r_d
                            po = list(map(str,position))
                            fo = open("calatter\\" + str(config.node_num) +".txt", "a")
                            curtime = datetime.datetime.now()
                            time = (curtime - starttime).seconds
                            fo.write(' '.join(po) + ' ' + str(max_qos) + ' ' + str(time) + ' ' + str(
                                k+ 1) + '\n')
                            print('calattar updated')
                            fo.close()
                        s_next=-1
                    else:
                        r_d=0
                        s_next=s+1
                    #存储进memory里（容量1000）
                    MEMORY[training_step % config.memory_capacity][0] = s
                    MEMORY[training_step % config.memory_capacity][1] = a_choosen
                    MEMORY[training_step % config.memory_capacity][2] = r_d
                    MEMORY[training_step % config.memory_capacity][3] = s_next

                    s = s + 1
                    training_step+=1

                    #train
                    if(training_step>=config.memory_capacity):
                        # 使targe q网络的参数等与q网络的参数
                        if training_step+1 % config.target_replace_iter == 0:
                            t_params = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='target_q')
                            e_params = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='q')
                            sess.run([tf.assign(t, e) for t, e in zip(t_params, e_params)])

                        #从memory里取[s,a,r,s+1]
                        sample_index = np.random.choice(config.memory_capacity)
                        train_data=MEMORY[sample_index]
                        state_m=train_data[0].astype(int)
                        a_m=train_data[1].astype(int)
                        r_m=train_data[2]
                        s_next_m=train_data[3].astype(int)

                        #得到maxQ(S+1,a)
                        q_target=0
                        if(s_next_m!=-1):
                            target_q_scores = sess.run(target_Q_scores, feed_dict={next_state: [s_next_m] })[0:num_service[s_next_m]]
                            a_choosen_target=np.argmax(target_q_scores)
                            q_target=sess.run(target_Q_score,feed_dict={next_state:[s_next_m],action:a_choosen_target})
                        #r+maxQ(S+1,a)
                        reward_y=r_m+q_target

                        loss,_=sess.run([optimize.loss,optimize.train_step],feed_dict={reward:reward_y,state:[state_m],action:a_m})

                        epsilon=epsilon+config.epsilon_increment if epsilon+config.epsilon_increment<config.max_epsilon else config.max_epsilon
                        #print(loss)
            print("Training COMPLETED !")

if __name__=="__main__":
    main()