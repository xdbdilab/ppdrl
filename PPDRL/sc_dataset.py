import numpy as np
import linecache
import tensorflow as tf


class SC_DataGenerator(object):
    np.random.seed(1)
    def gen_instance(self,dimension, f):  #dimension:服务质量类别数，f:nodeset.txt
        num_service = []  #各个服务的候选服务的数量
        service1 = []  # 某一服务的候选服务集的服务质量
        f.readline()
        line = f.readline()
        candidates_c = line.split(' ')
        candidates = [] #构成组合的所有服务的id
        for index in range(len(candidates_c)):
            candidates.append(candidates_c[index])
        for candidate in candidates:
            #print('candidate: ',candidate)
            num = 0
            f1 = open('服务名聚类最终结果/'+candidate+'.txt')
            line1 = f1.readline()
            while line1:
                num = num+1
                # atom = line1.split(':')[0]
                # the_line = linecache.getline('QWS_Dataset.txt', int(atom))
                # split_line1 = the_line.split(',')[1:dimension+1]
                # split_line = [float(c.encode("utf-8")) for c in split_line1]
                # service1.append(split_line)
                line1 = f1.readline()
            num_service.append(num)
        # service1 = np.array(service1)
        # service1 = ( service1-np.min(service1)) / (np.max(service1) - np.min(service1))  # 归一化 都是负的
        # service1 = service1.tolist()
        return num_service


    def train_batch(self, dimension, position, i):  #dimension:服务质量类别数
        f = open(position + '/' + i + '/nodeSet.txt')
        # Generate sc instance
        input_ = np.random.randn(1, 16)
        num = self.gen_instance(dimension, f)
        count = 0
        for i in num:
            count = count+i
        return input_, num, count  # input[sequence,5],num[nodenum]

if __name__ == "__main__":
    # position = tf.multinomial([[-1,0.2,0.3,0.4]], 1)
    # with tf.Session() as sess:
    #     print(sess.run(position))
    sc = SC_DataGenerator()
    input_,num,count = sc.train_batch(5,'test',12)
    print('input: ',input_)
    print('num: ',num)
    print('count: ',count)

