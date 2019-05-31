import tensorflow as tf

class Optimize(tf.keras.Model):
    def __init__(self, config):
        super(Optimize, self).__init__()
        with tf.variable_scope('optimize'):
            self.config=config
            self.lr = config.rl_lr  # initial learning rate

    def build_optim(self,reward,log_softmax):
        with tf.variable_scope('optimize'):
                self.loss = tf.reduce_mean(reward* log_softmax)
                '''tf.summary.scalar("actor_loss", self.loss)
                tf.summary.scalar('log_softmax', tf.reduce_mean(log_softmax))
                #tf.summary.scalar("avg_baseline", self.avg_baseline)
                tf.summary.scalar("reward", tf.reduce_mean(real))
                tf.summary.scalar("min_reward", tf.reduce_min(real))
                tf.summary.scalar("max_reward", tf.reduce_max(real))'''

                self.opt = tf.train.AdamOptimizer(learning_rate=self.lr,name='opt_rl')
                self.grads=self.opt.compute_gradients(self.loss,var_list=tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES,scope="actor"))
                self.train_step = self.opt.apply_gradients(self.grads)





