import numpy as np
import random
def calaulate(filepath, nodenum, filenum,n):
    qos = []
    qos_mean = 0
    qos_var = 0
    if n==4:
        for i in range(0,4):  #修改
            filename = filepath+'\calattar'+str(nodenum)+'_'+str(filenum)+'_'+str(i)+'.txt'
            file = open(filename,'r')
            lines = file.readlines()
            lastline = lines[-1]
            string = lastline.split()[nodenum]
            qos.append(float(string))
        qos_mean = np.mean(qos)
        qos_var = np.var(qos)
    else:
        for i in range(0,5):  #修改
            filename = filepath+'\calattar'+str(nodenum)+'_'+str(filenum)+'_'+str(i)+'.txt'
            file = open(filename,'r')
            lines = file.readlines()
            lastline = lines[-1]
            string = lastline.split()[nodenum]
            qos.append(float(string))
        qos_mean = np.mean(qos)
        qos_var = np.var(qos)
    return qos_mean,qos_var

def main():
    filepath = 'E:\司法业务协同服务\服务组合\实验结果\画图\ppdrl'  #修改
    nodenum_list = [10,30,50,70,90,100]
    filenum_list = [1,5,7,4,5,3]
    for n in range(6):
        nodenum = nodenum_list[n]
        filenum = filenum_list[n]
        qos_mean, qos_var = calaulate(filepath,nodenum,filenum,n)
        print(qos_mean,qos_var)

if __name__ == "__main__":
    main()  #修改

