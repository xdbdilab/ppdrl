import calattr
import random
import csv
# 改成当前结点
#NODE_NUM=100 # 改成结点
calattr = calattr.Calattr()
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
        f1 = open('julei_result/' + candidate + '.txt')
        line1 = f1.readline()
        while line1:
            num = num + 1
            line1 = f1.readline()
        num_service.append(num)
    return num_service

if __name__ =='__main__':
    calattr.init('test', 1)
    f = open('test/1/nodeSet.txt')
    num_service = Get_numservice(f)
    result=[]
    for i in range(64):
        print(i)
        pointer =[]
        for j in range(NODE_NUM):
            point = random.randint(0,num_service[j]-1)
            pointer.append(point)
        f = calattr.receive(pointer)
        pointer.append(f)
        result.append(pointer)

    '''def takeF(elem):
        return elem[-1]
    result.sort(key=takeF,reverse=True)'''
    result = result[:64]
    csvfile = open('init_data/init_data.csv', "w",newline="")
    writer = csv.writer(csvfile)
    writer.writerows(result)
    csvfile.close()



