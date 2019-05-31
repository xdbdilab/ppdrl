import tensorflow as tf

class Pretrain(tf.keras.Model):
    def __init__(self, config):
        super(Pretrain, self).__init__()
        with tf.variable_scope('p_optimize'):
            self.config=config
            self.node_num=config.node_num
            self.lr1_start = config.pretrain_lr

    def build_optim(self,outputs,label,num_service):
        with tf.variable_scope('p_optimize'):
            self.pretrain_loss =0
            before=0
            for j in range(self.node_num):
                y=label[j]
                self.pretrain_loss += -tf.reduce_sum(
                    tf.one_hot(y,num_service[j],1.0,0.0)*tf.log(
                        tf.nn.softmax(tf.slice(outputs,[before],[num_service[j]]) ))
                    )
                before+=num_service[j]
            self.opt = tf.train.AdamOptimizer(learning_rate=self.lr1_start,name='p_opt')
            self.pretrain_step = self.opt.minimize(self.pretrain_loss,var_list=tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES,scope="actor"))




