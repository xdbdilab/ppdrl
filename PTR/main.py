# -*- coding: utf-8 -*-

import tensorflow as tf
from newactor import Actor
from newoptimizer import Optimize
from sc_dataset import SC_DataGenerator
from config import get_config
from calattr import Calattr
from tqdm import tqdm
import numpy as np
import datetime
def main():

    # Get running configuration
    config, _ = get_config()


    input = tf.placeholder(tf.float32, [None, config.input_dimension], name="input_raw")
    reward=tf.placeholder(tf.float32,[config.sample_num],name="reward")
    num_service = tf.placeholder(tf.int32, [config.node_num], name="num_service")

    global_step = tf.Variable(0, trainable=False, name="global_step")

    actor = Actor(config)
    optimize = Optimize(config, global_step)

    training_set = SC_DataGenerator()
    position, softmax = actor(input,num_service)
    optimize.build_optim(reward, softmax)

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        sess.run(tf.local_variables_initializer())
        device = '/cpu:0'
        with tf.device(device):
            min = 100
            conf_dir = 'test//conf.xml'
            inputs, num = training_set.train_batch(config.input_dimension, 'test')
            calattr = Calattr()
            calattr.init(conf_dir, config.train_from)
            starttime = datetime.datetime.now()
            for i in tqdm(range(config.nb_epoch)):
                pos_list=sess.run(position, feed_dict={input: inputs,num_service:num})
                reward_list=[]
                for _ in range(config.sample_num):
                    f = calattr.receive(pos_list[_])#i+1
                    reward_list.append(-f)
                    if(min>-f):
                        min=-f
                        po = pos_list[_].astype(str)
                        fo = open("testlog\\new\\" + str(config.node_num) +".txt", "a")
                        curtime = datetime.datetime.now()
                        time=(curtime-starttime).seconds
                        fo.write(' '.join(po) + ' ' + str(-min) + ' ' + str(time)+ ' ' + str(i*config.node_num+_+1)+ '\n')
                        print('calattar updated')
                        fo.close()
                sess.run(optimize.train_step1,feed_dict={input: inputs,reward:reward_list,num_service:num})
            print("Training COMPLETED !")


if __name__ == "__main__":
    #tfe.enable_eager_execution()
    main()