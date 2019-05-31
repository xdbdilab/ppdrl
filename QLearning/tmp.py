# coding = utf - 8
"""
@author: LY
@contact: xdliyin@163.com
@version: 1.0
@time: 2019/5/8 21:50
"""
import pandas as pd
import numpy as np
k90 = 0
k91 = 0
k92 = 0
k93 = 0
k94 = 0
k95 = 0
k96 = 0
k97 = 0
k98 = 0
k99 = 0
for i in range(6000):
    tmp = np.random.uniform()
    if tmp >= 0.90:
        k90 += 1
    if tmp >= 0.91:
        k91 += 1
    if tmp >= 0.92:
        k92 += 1
    if tmp >= 0.93:
        k93 += 1
    if tmp >= 0.94:
        k94 += 1
    if tmp >= 0.95:
        k95 += 1
    if tmp >= 0.96:
        k96 += 1
    if tmp >= 0.97:
        k97 += 1
    if tmp >= 0.98:
        k98 += 1
    if tmp >= 0.99:
        k99 += 1


print("k 0.90 = {}".format(k90))
print("k 0.91 = {}".format(k91))
print("k 0.92 = {}".format(k92))
print("k 0.93 = {}".format(k93))
print("k 0.94 = {}".format(k94))
print("k 0.95 = {}".format(k95))
print("k 0.96 = {}".format(k96))
print("k 0.97 = {}".format(k97))
print("k 0.98 = {}".format(k98))
print("k 0.99 = {}".format(k99))


