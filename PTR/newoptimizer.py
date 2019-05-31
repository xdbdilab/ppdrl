import tensorflow as tf

class Optimize(tf.keras.Model):
    def __init__(self, config,global_step):
        super(Optimize, self).__init__()
        with tf.variable_scope('optimize'):
            self.config=config
            self.sample_num=config.sample_num
            self.alpha = config.alpha  # moving average update
            self.node_num=config.node_num
            self.avg_baseline = tf.Variable(config.init_baseline, trainable=False,name="moving_avg_baseline")  # moving baseline for Reinforce
            # Training config (actor)
            self.global_step = global_step  # global step
            self.lr1_start = config.lr1_start  # initial learning rate
            self.lr1_decay_rate = config.lr1_decay_rate  # learning rate decay rate
            self.lr1_decay_step = config.lr1_decay_step  # learning rate decay step




    def build_optim(self,reward,log_softmax):
        with tf.variable_scope('optimize'):
            self.avg_baseline=self.alpha * self.avg_baseline + (1.0 - self.alpha) * tf.reduce_mean(reward)
            reward_bs = reward - self.avg_baseline
            self.loss1 = tf.reduce_mean(reward_bs * log_softmax)
            self.lr1 = tf.train.exponential_decay(self.lr1_start, self.global_step, self.lr1_decay_step,self.lr1_decay_rate, staircase=False, name="learning_rate1")
            # Optimizer
            self.opt1 = tf.train.AdamOptimizer(learning_rate=self.lr1,name='opt1')
            # Loss
            self.train_step1 = self.opt1.minimize(self.loss1,global_step=self.global_step,var_list=tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES,scope="actor"))