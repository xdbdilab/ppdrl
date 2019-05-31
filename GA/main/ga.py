import newga
import time
import numpy as np
import random
import csv
import calattr
import main.generate as ge
#节点数（按需要修改）
NODE_NUM=100
#每个节点的测试组数根据不同测试集做修改
TEST_GROUP_NUM=11
for n in range(1,TEST_GROUP_NUM):
    timstart =time.time()

    ge.calattr.init('test//%d'%NODE_NUM,n,NODE_NUM)

    path ='test/'+str(NODE_NUM)+'/%d/nodeSet.txt'%n
    f = open(path)
    num_service = ge.Get_numservice(f)
    result = []
    for i in range(64):
        print(i)
        pointer = []
        for j in range(NODE_NUM):
            point = random.randint(0, num_service[j] - 1)
            pointer.append(point)
        f = ge.calattr.receive(pointer)
        pointer.append(f)
        result.append(pointer)

    '''def takeF(elem):
        return elem[-1]
    result.sort(key=takeF,reverse=True)'''
    result = result[:64]
    csvfile = open('init_data/init_data.csv', "w", newline="")
    writer = csv.writer(csvfile)
    writer.writerows(result)
    csvfile.close()

    a ,calNum = newga.GA(n,num_service,timstart)
    #返回结果
    timeresult = time.time()-timstart
    print(n,a,calNum,timeresult)
#     trs = str([n, a])

#     fname = './result/ga%d.txt'%NODE_NUM
#     try:
#         fobj = open(fname, 'a')  # 这里的a意思是追加，这样在加了之后就不会覆盖掉源文件中的内容，如果是w则会覆盖。
#     except IOError:
#         print('file open error:')
#     else:
#         #  这里的\n的意思是在源文件末尾换行，即新加内容另起一行插入。
#         fobj.write(trs)
#         fobj.write(str(timeresult)+" calNum:")
#         fobj.write(str(calNum))
#
#     fobj.write('\n')
# fobj.close()

