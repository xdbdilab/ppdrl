import calattr
import numpy
import numpy as np
import time
import csv
'''
分支限界法
'''
#节点数按需修改
Node_number=100
#测试组数
TEST_GROUP_NUM =11
calattr = calattr.Calattr()

def Get_numservice(f):
    num_service = []
    f.readline()
    line = f.readline()
    candidates_c = line.split(' ')
    candidates = []
    for index in range(len(candidates_c)):
        candidates.append(candidates_c[index])
    #print('Candidates: ',candidates)
    for candidate in candidates:
        num = 0
        # rows = 0  # 使得服务限制在2个
        f1 = open('julei_result/' + candidate + '.txt')
        line1 = f1.readline()
        while line1:
            num = num + 1
            line1 = f1.readline()
        num_service.append(num)
    return num_service

def translateDNA(x,num_service):
    x_out=[]
    print(num_service)
    for i in range(len(num_service)):
        x_out.append(np.maximum(int(
            np.floor(x[i] * num_service[i]-0.0001)
        ),0))
    return x_out

def branch(nodeset ,number,NODE_NUM,startTime):

    #初始化
    calattr.init('test//%d' % NODE_NUM, number, NODE_NUM)
    inition = np.zeros(NODE_NUM+1)
    inition_one=np.zeros(NODE_NUM,numpy.int8)
    initionsum = np.random.random(size=(1,NODE_NUM))
    inition_one[0:NODE_NUM] = translateDNA(initionsum[0],nodeset)
    inition[0:NODE_NUM] =inition_one[0:NODE_NUM]
    inition[-1]=calattr.receive(inition_one[0:NODE_NUM])
    evalation=0;
    for i in range(len(nodeset)):
        nodeset_fu = []
        for p in range(len(nodeset)):
            nodeset_fu.append(int(nodeset[p]))
        for j in range(nodeset[i]):
            evalation=evalation+1
            print("the j is%d"%j)
            inition_two =np.zeros(NODE_NUM+3)
            inition_three =np.zeros(NODE_NUM+1,numpy.int8)
            for v in range(len(inition)):
                inition_two[v]=inition[v]
            inition_two[i]=j
            for m in range(len(inition_three)):
                inition_three[m]=(int)(inition_two[m])
            inition_two[-3]=(calattr.receive(inition_three[0:NODE_NUM]))
            print("the inition :"+str(inition))
            print("the inition_two ;"+str(inition_two))
            if(float(inition_two[-3])>float(inition[-1])):
                timePrice = time.time()-startTime
                for n in range(len(inition)):
                    inition[n]=inition_two[n]
                pathResult='./InBranchresult/result'+str(NODE_NUM)+'_%d.txt'%number
                try:
                    fobj = open(pathResult, 'a')  # 这里的a意思是追加，这样在加了之后就不会覆盖掉源文件中的内容，如果是w则会覆盖。
                   #csvFile2 = open(pathResult, 'a', newline='')
                except IOError:
                    print('file open error:')
                else:
                    #  这里的\n的意思是在源文件末尾换行，即新加内容另起一行插入。
                    fobj.write(str(inition_three[0:NODE_NUM]))
                    fobj.write(" ")
                    fobj.write(str(inition_two[-3]))
                    fobj.write(" ")
                    fobj.write(str(timePrice))
                    fobj.write(" ")
                    fobj.write(str(evalation))
                    fobj.write('\n')
                    print("insert ok")
                    fobj.close()

            else:
                print("wei zhuang aaaaaaaaaaaa")
                continue
    return inition
for i in range(1,TEST_GROUP_NUM):
    startTime=time.time()
    path ='./test/'+str(Node_number)+'/%d/nodeSet.txt'%i
    f=open(path)
    nodse1=Get_numservice(f)
    print(nodse1)
    a = branch(nodse1,i,Node_number,startTime)