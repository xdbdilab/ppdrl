# -*- coding: utf-8 -*-

import tensorflow as tf
from actor import Actor
from optimizer import Optimize
from config import get_config
import numpy as np
from sc_dataset import SC_DataGenerator
from calattr import Calattr
from pretrain import Pretrain
import csv
import random
import time
import os
import generate



def main(config,calattr,inputs,num,evaluations_number):
    tf.reset_default_graph()
    # Get running configuration
    start = time.time()
    # training_set = SC_DataGenerator()
    # inputs, num, count = training_set.train_batch(config.input_dimension, config.train_from, config.ist_nodeset)
    # config.all_node_num = count
    input = tf.placeholder(tf.float32, [1, 16], name="input_raw")
    num_service = tf.placeholder(tf.int32, [config.node_num], name="num_service")
    reward = tf.placeholder(tf.float32, [config.sample_num], name="reward")
    label = tf.placeholder(tf.int32,[config.node_num], name="label")
    #real_re = tf.placeholder(tf.float32, [config.sample_num], name="reward_real")

    actor = Actor(config)
    pre = Pretrain(config)
    optimize = Optimize(config)

    pos, logsoftmax, scores = actor(input, num_service)
    optimize.build_optim(reward, logsoftmax)
    pre.build_optim(scores,label,num_service)
    #saver = tf.train.Saver(max_to_keep=0)

    # inputs, num, count = training_set.train_batch(config.input_dimension, config.train_from, config.ist_nodeset)
    # config.all_node_num = count
    #print('inputs: ',inputs)
    # calattr = Calattr()
    # calattr.init(config.train_from, config.ist_nodeset)
    min = 0
    with tf.Session() as sess:
        for iter_cur in range(config.iter_num):
            print('====================================iter ' + str(iter_cur + 1) + ' =====================================')
            #writer = tf.summary.FileWriter(config.log_dir, sess.graph)
            #merged = tf.summary.merge(tf.get_collection(tf.GraphKeys.SUMMARIES, 'optimize'))
            if (iter_cur == 0):
                sess.run(tf.global_variables_initializer())
                sess.run(tf.local_variables_initializer())
                print('var initialized')
            #else:
                #saver.restore(sess, tf.train.latest_checkpoint(config.restore_from + '/'))
                #print("Model restored.")
            #device = '/cpu:0'
            #with tf.device(device):
            print('==================================== pretraining =====================================')
            with open(config.result_dir, "r") as csvfile:
                reader = csv.reader(csvfile)
                result = list(reader)
            for i in range(config.pretrain_epoch):
                #print('pretraining iter ' + str(i + 1))
                #rand = random.randint(0, config.best_num-1)   change!!!!!!!!!!!
                rand_label=result[i%64][:config.node_num]
                rand_label=list(map(int,rand_label))
                _,score=sess.run([pre.pretrain_step,scores], feed_dict={input: inputs, num_service: num,label:rand_label})
            #saver.save(sess, config.save_to + "/model_pretrain.ckpt")
            #print('saved mode')
            print('==================================== pretrain completed =====================================')
            ##############################rl#########################
            print('==================================== reinforcement learning =====================================')
            #min=0   change!!!!!!!!!!
            pointer = []
            for rl in range(config.rl_epoch):
                #print('reinforcement iter '+str(rl+1))
                pos_list, probs = sess.run([pos, actor.prob],feed_dict={input: inputs, num_service: num})
                reward_list = []
                real_reward=[]
                for _ in range(config.sample_num):
                    point = []
                    for l in range(config.node_num):
                        point.append(pos_list[_][l])
                    f = calattr.receive(pos_list[_])  # i+1
                    evaluations_number = evaluations_number + 1
                    point.append(f)
                    pointer.append(point)
                    real_reward.append(-f)
                    reward_list.append(-f)
                    if (min > -f):
                            min = -f
                            po=pos_list[_].astype(str)
                            fo = open(config.temp_best_dir, "a")
                            fo.write(' '.join(po) + ' ' + str(-min) + ' ' + str(time.time() - start) + ' '+ str(evaluations_number) + '\n')
                            fo.close()
                            #print('calattar updated')

                mean=np.mean(reward_list)
                reward_list=reward_list-mean

                #print('prob:', probs)
                grads, _ = sess.run(
                        [optimize.grads, optimize.train_step],
                        feed_dict={input: inputs, reward: reward_list, num_service: num})
                #writer.add_summary(summary, i + 1)

            def takeF(elem):
                return elem[-1]
            with open(config.result_dir, "r") as csvfile:
                reader = csv.reader(csvfile)
                before_result = list(reader)
                for q in range(config.best_num):
                    b_re = before_result[q]
                    int_line = list(map(int, b_re[:config.node_num]))
                    int_line.append(float(b_re[-1]))
                    #print('int_line: ',int_line)
                    pointer.append(int_line)
            pointer = list(set([tuple(t) for t in pointer]))
            pointer.sort(key=takeF, reverse=True)
            pointer = pointer[:config.best_num]

            csvfile = open(config.result_dir, "w", newline="")
            writer = csv.writer(csvfile)
            writer.writerows(pointer)
            csvfile.close()
            print("WRITED IN SUIJI CSV !")
            #saver.save(sess, config.save_to + "/model_over.ckpt")
            print('==================================== reinforcement completed =====================================')



if __name__ == "__main__":
    #tfe.enable_eager_execution()
    node = '10'
    config, _ = get_config()
    config.node_num = int(node)
    rootdir = 'testmore/'+node
    calattr = Calattr()
    training_set = SC_DataGenerator()
    for num in range(5):
        for listFile in os.listdir(rootdir):
            evaluations_number = 0
            print(listFile)
            config.ist_nodeset = node + '/' + listFile
            #print('nodeset: ',config.ist_nodeset)
            config.temp_best_dir = 'testlog/new/calattar'+node+'_'+listFile+'_'+str(num)+'.txt'
            calattr.init(config.node_num, config.train_from, config.ist_nodeset)
            generate.generate_data(calattr,config)
            inputs, num, count = training_set.train_batch(config.input_dimension, config.train_from, config.ist_nodeset)
            config.all_node_num = count
            main(config,calattr,inputs,num,evaluations_number)
