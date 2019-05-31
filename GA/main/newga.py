import time
import numpy as np
import math
import calattr
import csv
# 节点个数（要修改）
NODE_NUM=100
DNA_SIZE = NODE_NUM+1            # DNA length
POP_SIZE = 64          # population size
CROSS_RATE = 0.5         # mating probability (DNA crossover)
MUTATION_RATE = 0.2    # mutation probability

#迭代次数
N_GENERATIONS =6000    # 4000
calattr = calattr.Calattr()

def Get_numservice(f):
    num_service = []
    f.readline()
    line = f.readline()
    candidates_c = line.split(' ')
    candidates = []
    for index in range(len(candidates_c)):
        candidates.append(candidates_c[index])
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




#########
num_service = []

#遗传算法的编码方法
def translateDNA(x,num_service):
    x_out=[]
    for i in range(NODE_NUM):
        x_out.append(np.maximum(int(
            np.floor(x[i] * num_service[i]-0.0001)
        ),0))
    return x_out


def get_fcost(pop,num_service):
    out=[]
    for k in range(len(pop)):
        temp=[]
        for n in range(NODE_NUM):
            temp.append(pop[k][n]/num_service[n])
        temp.append(pop[k][-1])
        out.append(temp)
    return out

#遗传
def crossover(i,n,pop):
    c1=np.zeros(DNA_SIZE)
    c2=np.zeros(DNA_SIZE)
    c1[0:int(NODE_NUM/2)]=pop[i][0:int(NODE_NUM/2)]
    c1[int(NODE_NUM/2):NODE_NUM]=pop[n][int(NODE_NUM/2):NODE_NUM]
    c2[0:int(NODE_NUM/2)]=pop[n][0:int(NODE_NUM/2)]
    c2[int(NODE_NUM/2):NODE_NUM]=pop[i][int(NODE_NUM/2):NODE_NUM]
    return c1,c2

#变异
def mutate(i,pop):
    c1=np.zeros(DNA_SIZE)
    for m in range(DNA_SIZE-1):
        if np.random.rand() < MUTATION_RATE:
            c1[m]=np.random.rand()
        else:
            c1[m]=pop[i][m]
    return c1

#遗传算法入口
def GA(number,num_service,startTime):
    # path ='test/10/%d/nodeSet.txt'%number
    # f = open(path)
    # num_service = Get_numservice(f)

    #初始化（要修改）

    calattr.init('test//%d'%NODE_NUM,number,NODE_NUM)
    #pop = np.random.random(size=(POP_SIZE ,DNA_SIZE))#[50,31]   这里是随机的算子
    pop_before=[]
    T1_cost=[]
    with open('init_data//init_data.csv', "r") as csvfile:
        reader = csv.reader(csvfile)
        before_result = list(reader)
        for q in range(before_result.__len__()):
            b_re = before_result[q]
            T1_cost.append(float(b_re[-1]))

            int_line = list(map(float, b_re[:NODE_NUM]))
            int_line.append(float(b_re[-1]))
            pop_before.append(int_line)

    pop=get_fcost(pop_before,num_service)
    off_pop =pop
    getfit = 0
    calNum=0
    for g in range(N_GENERATIONS):
        print('iter '+str(g+1))
        pop = off_pop
        T3_cost=[]
        for i in range(1,int(len(pop)/2)):
             n = np.random.randint(0, POP_SIZE)
             if  (np.random.rand() < CROSS_RATE):
                    child1,child2=crossover(i,n,pop)
             else:
                child1=mutate(i,pop)
                child2=mutate(n,pop)

             child1[-1]=calattr.receive(translateDNA(child1,num_service))
             child2[-1] = calattr.receive(translateDNA(child2,num_service))

             pop = np.vstack((pop, child1))
             pop = np.vstack((pop, child2))
        print(i)

        for i in range(len(pop)):
            T3_cost.append(pop[i][ -1])
        T3_cost.sort()

        p = 0
        for i in range(len(pop)):
            if (T3_cost.index(pop[i][-1])>int(len(T3_cost)/2)):
                off_pop[p]=pop[i]
                p=p+1

        for i in range(len(pop)):
            if (pop[i][-1]==T3_cost[-1]):
                fitness=pop[i].copy()#这是引用！！！！！！！！！！！！！！！


        #解码过程
        for i in range(NODE_NUM):
            position=np.maximum(int(np.floor(fitness[i] * num_service[i]-0.0001)),0)
            fitness[i]=position
        print('the Gen is:%d' % g)
        print(fitness)
        if(fitness[-1]>getfit):
           timeresult = time.time() - startTime
           pathResult ='./result/result'+str(NODE_NUM)+'_%d.txt'%number
           insert_Set=[]
           m = len(fitness)
           for i in range(m-1):
                insert_Set.append((int)(fitness[i]))
           insert_Set.append(fitness[-1])
           insert_Set.append(timeresult)
           insert_Set.append(g*POP_SIZE)


           try:
               fobj = open(pathResult, 'a')  # 这里的a意思是追加，这样在加了之后就不会覆盖掉源文件中的内容，如果是w则会覆盖。
           except IOError:
               print('file open error:')
           else:
               #  这里的\n的意思是在源文件末尾换行，即新加内容另起一行插入。
               fobj.write(str(insert_Set))
           fobj.write('\n')
           print("insert ok")
           fobj.close()
           getfit = fitness[-1]
        # csvFile2 = open(pathResult, 'a',newline='')  # 设置newline，否则两行之间会空一行
        # writer = csv.writer(csvFile2)
           # writer.writerow(insert_Set)
           # print("change ok !")
           #getfit =fitness[-1]
           # #calNum =g;
           # csvFile2.close()

    return fitness , calNum



