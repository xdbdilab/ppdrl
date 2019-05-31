import tensorflow as tf

class Optimize(tf.keras.Model):
    def __init__(self, config,global_step):
        super(Optimize, self).__init__()
        with tf.variable_scope('optimize'):
            self.config=config

            self.global_step = global_step  # global step
            self.lr_start = config.lr_start  # initial learning rate
            self.lr_decay_rate = config.lr_decay_rate  # learning rate decay rate
            self.lr_decay_step = config.lr_decay_step  # learning rate decay step

    def build_optim(self,y,Q_score):
        with tf.variable_scope('optimize'):
            self.loss =(y-Q_score)**2
            self.lr = tf.train.exponential_decay(self.lr_start, self.global_step, self.lr_decay_step,self.lr_decay_rate, staircase=False, name="learning_rate")
            # Optimizer
            self.opt = tf.train.AdamOptimizer(learning_rate=self.lr,name='opt')
            # Loss
            self.train_step = self.opt.minimize(self.loss,global_step=self.global_step,var_list=tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES,scope="q"))