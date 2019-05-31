# -*- coding: utf-8 -*-

import tensorflow as tf
distr = tf.contrib.distributions
from tensorflow.contrib.rnn import LSTMCell

class Qnetwork(tf.keras.Model):
    def __init__(self, config,scope,max_action_num):
        super(Qnetwork, self).__init__()
        self.scope=scope
        with tf.variable_scope(self.scope):
            self.config=config
            self.max_action_num=max_action_num
            self.LSTM_dim = config.hidden_dim
            self.initializer = tf.contrib.layers.xavier_initializer()  # variables initializer
            self.cell=LSTMCell(self.LSTM_dim,initializer=self.initializer)
            self.fn_layer=tf.layers.Dense(30,activation=tf.nn.tanh,name='fn_layer')
            self.out_layer = tf.layers.Dense(max_action_num, name='out_layer')

    def get_q_score(self,state,a):
        self.get_q_scores(state)
        return self.Q_score[a]

    def get_q_scores(self,state_input):
        with tf.variable_scope(self.scope):
            state_input=tf.expand_dims(state_input,axis=0)
            zero_state=self.cell.zero_state(batch_size=1,dtype=tf.float32)
            encoder_output, states = self.cell(state_input,zero_state)
            fn_input = states.h  #
            out_input=self.fn_layer(fn_input)
            self.Q_score=tf.squeeze(self.out_layer(out_input))
            return self.Q_score






