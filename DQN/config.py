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
net_arg.add_argument('--hidden_dim', type=int, default=30, help='actor LSTM num_neurons') #128

# Data
data_arg = add_argument_group('Data')
data_arg.add_argument('--node_num', type=int, default=10, help='node num')

# Training / test parameters
train_arg = add_argument_group('Training')
train_arg.add_argument('--nb_epoch', type=int, default=100000, help='nb epoch')
train_arg.add_argument('--lr_start', type=float, default=0.0002, help='actor learning rate')#
train_arg.add_argument('--lr_decay_step', type=int, default=5000, help='lr1 decay step')
train_arg.add_argument('--lr_decay_rate', type=float, default=0.96, help='lr1 decay rate')

train_arg.add_argument('--max_epsilon', type=float, default=0.9, help='max_epsilon')#
train_arg.add_argument('--min_epsilon', type=float, default=0.1, help='min_epsilon')#
train_arg.add_argument('--epsilon_increment', type=float, default=0.01, help='epsilon')#
train_arg.add_argument('--memory_capacity', type=int, default=300, help='memory_capacity')#
train_arg.add_argument('--target_replace_iter', type=int, default=50, help='target_replace_iter')#
# Misc
misc_arg = add_argument_group('User options') #####################################################
misc_arg.add_argument('--train_from', type=str, default='data', help='train data position')#test



def get_config():
  config, unparsed = parser.parse_known_args()
  return config, unparsed
