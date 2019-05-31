from calattr import Calattr
import random
import csv
from config import get_config


def Get_numservice(f):
    num_service = []
    f.readline()
    line = f.readline()
    candidates_c = line.split(' ')
    candidates = []
    for index in range(len(candidates_c)):
        candidates.append(candidates_c[index])
    # print('Candidates: ',candidates)
    for candidate in candidates:
        num = 0
        # rows = 0  # 使得服务限制在2个
        f1 = open('服务名聚类最终结果/' + candidate + '.txt')
        line1 = f1.readline()
        while line1:
            num = num + 1
            line1 = f1.readline()
        num_service.append(num)
    return num_service

#if __name__ =='__main__':
def generate_data(calattr,config):
    path = config.train_from+"/"+config.ist_nodeset+"/nodeSet.txt"
    #print('path: ',path)
    f = open(path)
    num_service = Get_numservice(f)
    result=[]
    for i in range(config.init_gen_num):
        #print(i)
        pointer =[]
        for j in range(config.node_num):
            point = random.randint(0,num_service[j]-1)
            pointer.append(point)
        f = calattr.receive(pointer)
        pointer.append(f)
        result.append(pointer)

    def takeF(elem):
        return elem[-1]
    result.sort(key=takeF,reverse=True)
    result = result[:config.best_num]
    csvfile = open(config.result_dir, "w",newline="")
    writer = csv.writer(csvfile)
    writer.writerows(result)
    csvfile.close()


