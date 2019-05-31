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


# Data
data_arg = add_argument_group('Data')
data_arg.add_argument('--input_dimension', type=int, default=5, help='Number of service quality categories') #5
data_arg.add_argument('--node_num', type=int, default=100, help='Service number of web composition')  #30  需要修改
data_arg.add_argument('--all_node_num', type=int, default=858, help='All web number')  #414

# Training / test parameters
train_arg = add_argument_group('Training')
train_arg.add_argument('--iter_num', type=int, default=100, help='The iter number of pretrain and rl')  #100:30 90:60 70:100
train_arg.add_argument('--pretrain_epoch', type=int, default=360, help='pretrain epoch') #change!!!!!!!!!!!!
train_arg.add_argument('--rl_epoch', type=int, default=300, help='rl epoch')  #300
train_arg.add_argument('--rl_lr', type=float, default=0.0001, help='rl learning rate')#0.0001
train_arg.add_argument('--pretrain_lr', type=float, default=0.001, help='pretrain learning rate')#0.0001
train_arg.add_argument('--C', type=float, default=3, help='pointer_net tan clipping')#2
train_arg.add_argument('--sample_num', type=int, default=64, help='rl sample number')
train_arg.add_argument('--best_num', type=int, default=64, help='Number of best results')
train_arg.add_argument('--init_gen_num', type=int, default=50000, help='Number of generated data') #50000

# Misc
misc_arg = add_argument_group('User options')
misc_arg.add_argument('--save_to', type=str, default='10/model3', help='saver directory')
misc_arg.add_argument('--restore_from', type=str, default='10/model3', help='loader directory')
misc_arg.add_argument('--log_dir', type=str, default='summary/10/repo', help='summary directory')
misc_arg.add_argument('--train_from', type=str, default='test', help='data position')#test
misc_arg.add_argument('--ist_nodeset', type=str, default='12', help='the ist nodeset.txt')#1
misc_arg.add_argument('--result_dir', type=str, default='pretrain/result.csv', help='result directory')
misc_arg.add_argument('--temp_best_dir', type=str, default='testlog/new/calattar.txt', help='temp best result directory')

def get_config():
  config, unparsed = parser.parse_known_args()
  return config, unparsed
