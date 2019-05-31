# -*- coding: utf-8 -*-

import tensorflow as tf
distr = tf.contrib.distributions

class Actor(tf.keras.Model):
        def __init__(self, config):
                super(Actor, self).__init__()
                with tf.variable_scope('actor'):
                    self.config=config
                    self.input_dimension = config.input_dimension  # Number of service quality categories  5
                    self.initializer = tf.contrib.layers.xavier_initializer()  # variables initializer
                    self.node_num=config.node_num
                    self.sample_num=config.sample_num
                    self.C=config.C
                    self.all_node_num=config.all_node_num
                    print(self.all_node_num)

        def call(self,inputs,num_service):#inputs:[sequence,dimension]
            with tf.variable_scope('actor'):
                self.log_softmaxs = []
                self.positions = []
                #inputs=tf.reshape(inputs,[self.all_node_num*self.input_dimension])
                #inputs=tf.expand_dims(inputs,axis=0)
                # layer2=tf.layers.dense(inputs,self.all_node_num*5,name='fn1',activation=tf.nn.tanh)   change!!!!!!!!!!!
                # layer3 = tf.layers.dense(layer2, self.all_node_num*4,name='fn2',activation=tf.nn.tanh)
                # layer4 = tf.layers.dense(layer3, self.all_node_num*3,name='fn3',activation=tf.nn.tanh)
                # layer5 =tf.layers.dense(layer4, self.all_node_num*2, name='fn4')
                # layer6 = tf.layers.dense(layer5, self.all_node_num, name='fn5')
                #print('inputs: ',inputs)
                layer2 = tf.layers.dense(inputs,128,name='fn1',activation=tf.nn.tanh)
                layer3 = tf.layers.dense(layer2,self.all_node_num,name='fn2')
                #print('layer3: ',layer3)
                scores = tf.squeeze(layer3)  # [seq_length]
                scores = self.C*tf.nn.tanh(scores)

                before = 0
                for k in range(self.node_num):
                    # decode
                    temp_choose = tf.slice(scores, [before], [num_service[k]])  # temp_choose:[temp_sequence]
                    if(k==5):
                        self.prob = tf.nn.softmax(temp_choose)
                    prob = distr.Categorical(temp_choose)
                    position = prob.sample(self.sample_num)
                    log_softmax = prob.log_prob(position)
                    self.log_softmaxs.append(log_softmax)

                    self.positions.append(position)
                    before = before + num_service[k]
                self.log_softmax = tf.reduce_sum(self.log_softmaxs, axis=0)

                return tf.transpose(self.positions), self.log_softmax,scores






