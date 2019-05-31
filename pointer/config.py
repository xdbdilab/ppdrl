#-*- coding: utf-8 -*-
import argparse
import numpy as np

parser = argparse.ArgumentParser(description='Configuration file')
arg_lists = []


def add_argument_group(name):
  arg = parser.add_argument_group(name)
  arg_lists.append(arg)
  return arg


def str2bool(v):
  return v.lower() in ('true', '1')


# Network
net_arg = add_argument_group('Network')
net_arg.add_argument('--hidden_dim', type=int, default=128, help='actor LSTM num_neurons') #128
net_arg.add_argument('--hidden_dim_LSTM', type=int, default=128, help='actor LSTM num_neurons') #128

# Data
data_arg = add_argument_group('Data')
data_arg.add_argument('--input_dimension', type=int, default=5, help='Number of service quality categories') #5   有一个是后面五个算出来的
data_arg.add_argument('--node_num', type=int, default=10, help='node num')  #！！！!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# Training / test parameters
train_arg = add_argument_group('Training')
train_arg.add_argument('--nb_epoch', type=int, default=10000, help='nb epoch')
train_arg.add_argument('--lr1_start', type=float, default=0.0001, help='actor learning rate')#0.0001
train_arg.add_argument('--lr1_decay_step', type=int, default=1000, help='lr1 decay step')
train_arg.add_argument('--lr1_decay_rate', type=float, default=0.96, help='lr1 decay rate')

train_arg.add_argument('--alpha', type=float, default=0.9, help='update factor moving average baseline')#0.5
train_arg.add_argument('--init_baseline', type=float, default=0.0, help='initial baseline - REINFORCE')#7.0

train_arg.add_argument('--C', type=float, default=3, help='pointer_net tan clipping')
train_arg.add_argument('--sample_num', type=int, default=128, help='training sample number')



# Misc
misc_arg = add_argument_group('User options') #####################################################
misc_arg.add_argument('--train_from', type=str, default='test', help='train data position')#test



def get_config():
  config, unparsed = parser.parse_known_args()
  return config, unparsed


def print_config():
  config, _ = get_config()
  print('\n')
  print('Data Config:')
  print('* Batch size:',config.batch_size)
  print('* Sequence length:',config.max_length)
  print('* City coordinates:',config.input_dimension)
  print('\n')
  print('Network Config:')
  print('* Restored model:',config.restore_model)
  print('* Actor hidden_dim (embed / num neurons):',config.hidden_dim)
  #print('* Actor tan clipping:',config.C)
  print('\n')
  if config.inference_mode==False:
  	print('Training Config:')
  	print('* Nb epoch:',config.nb_epoch)
#  	print('* Temperature:',config.temperature)
  	print('* Actor learning rate (init,decay_step,decay_rate):',config.lr1_start,config.lr1_decay_step,config.lr1_decay_rate)
  else:
  	print('Testing Config:')
  print('* Summary writer log dir:',config.log_dir)
  print('\n')