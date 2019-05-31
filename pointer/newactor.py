# -*- coding: utf-8 -*-

import tensorflow as tf
distr = tf.contrib.distributions
from tensorflow.contrib.rnn import LSTMCell,LayerNormBasicLSTMCell,BasicLSTMCell

class Actor(tf.keras.Model):
        def __init__(self, config):
                super(Actor, self).__init__()
                with tf.variable_scope('actor'):
                    self.config=config
                    self.input_dimension = config.input_dimension  # Number of service quality categories  5
                    self.input_embed = config.hidden_dim  # dimension of embedding space (actor)  128
                    self.LSTM_dim = config.hidden_dim_LSTM  # dimension of embedding space (actor)  128
                    self.initializer = tf.contrib.layers.xavier_initializer()  # variables initializer
                    self.node_num=config.node_num
                    self.cell=LSTMCell(self.LSTM_dim,initializer=self.initializer)
                    self.sample_num=config.sample_num
                    self.W_embed = tf.get_variable("W_embed", [self.input_dimension, self.input_embed],
                                           initializer=self.initializer, trainable=True,dtype=tf.float32)
                    self.b_embed = tf.get_variable("b_embed", [self.input_embed],
                                                   initializer=self.initializer, trainable=True,dtype=tf.float32)
                    self.C=config.C
                    self.layer1=tf.layers.Dense(self.LSTM_dim,activation=tf.nn.tanh,name='layer1')
                    self.layer2 = tf.layers.Dense(self.LSTM_dim, activation=tf.nn.tanh, name='layer2')
                    self.W_ref = tf.get_variable("W_ref", [self.LSTM_dim, self.LSTM_dim],
                                                 initializer=self.initializer,dtype=tf.float32)
                    self.W_ref_b = tf.get_variable("W_ref_b", [self.LSTM_dim],
                                                 initializer=self.initializer, dtype=tf.float32)
                    self.W_q = tf.get_variable("W_q", [self.LSTM_dim, self.LSTM_dim], initializer=self.initializer,dtype=tf.float32)
                    self.W_q_b = tf.get_variable("W_q_b", [self.LSTM_dim],
                                               initializer=self.initializer, dtype=tf.float32)
                    self.v = tf.get_variable("v", [self.LSTM_dim,1], initializer=self.initializer,dtype=tf.float32)
        def call(self,inputs,num_service):#inputs:[sequence,dimension]
            with tf.variable_scope('actor'):
                self.log_softmaxs = []
                self.positions = []

                # Embed input sequence
                embedded_inputs = tf.nn.tanh(tf.matmul( inputs, self.W_embed)+self.b_embed)#embedded_inputs:[sequence,hidden_dim]
                embedded_inputs=tf.expand_dims(embedded_inputs,axis=0)#[1,sequence,hidden_dim]
                encoder_output, states = tf.nn.dynamic_rnn(self.cell,embedded_inputs,dtype=tf.float32)
                final_out = tf.reduce_mean(encoder_output,axis=1)  # [1,256]
                layer1=self.layer1(final_out)
                layer2 = self.layer2(layer1)

                encoder_output = tf.squeeze(encoder_output)

                encoded_ref = tf.matmul(encoder_output, self.W_ref,name="encoded_ref")+self.W_ref_b# [seq_length, n_hidden]
                encoded_query = tf.matmul(layer2, self.W_q,name="encoded_query")+self.W_q_b# [1, n_hidden]
                scores = tf.matmul(tf.nn.tanh(encoded_ref + encoded_query),self.v)
                scores = tf.squeeze(scores)
                scores=self.C*tf.nn.tanh(scores)

                before=0
                for k in range(self.node_num):
                    temp_choose =tf.slice(scores,[before],[num_service[k]])#temp_choose:[temp_sequence]
                    prob =distr.Categorical(temp_choose)
                    position = prob.sample(self.sample_num)
                    log_softmax=prob.log_prob(position)
                    self.log_softmaxs.append(log_softmax)
                    self.positions.append(position)
                    before =before+ num_service[k]
                self.log_softmax = tf.reduce_sum(self.log_softmaxs,axis=0)
                return  tf.transpose(self.positions),self.log_softmax






