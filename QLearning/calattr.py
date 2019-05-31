import xml.dom.minidom
import os

MAX_SERVICE = 100
MAX_NODE = 200
NODE_SET = 233
TOTAL_NODE = 2507
NODE_TRANS_INVALID = 9999


class Service(object):
    def __init__(self):
        self.index = 0
        self.id = 0
        self.RT = 0
        self.maxRT = 0
        self.minRT = 0
        self.throughput = 0
        self.maxThrou = 0
        self.minThrou = 0
        self.children = []
        self.parents = []


class ResultSet(object):
    def __init__(self):
        self.time = 0
        self.throu = 0
        self.cost = 0
        self.reli = 0
        self.success = 0
        self.avail = 0


class Node(object):
    def __init__(self):
        self.id = 0
        self.responseTime = 0
        self.throughput = 0
        self.availabilit = 0
        self.successability = 0
        self.reliability = 0
        self.price = 0


class Set(object):
    def __init__(self):
        self.id = 0
        self.maxTime = 0
        self.minTime = 0
        self.maxThroughput = 0
        self.minThroughput = 0
        self.maxAvailability = 0
        self.minAvailability = 0
        self.maxSuccessability = 0
        self.minSuccessability = 0
        self.maxReliability = 0
        self.minReliability = 0
        self.maxPrice = 0
        self.minPrice = 0


class ServiceInfoFromConf(object):
    def __init__(self):
        self.index = 0
        self.id = 0


class Calattr(object):
    def __init__(self,conf_file, nodeSet_file):
        self.conf_file = conf_file
        self.nodeSet_file = nodeSet_file
        self.serviceNum = 0
        self.mServiceMap = {}
        self.nodeSet = []
        self.serviceNode = []
        self.graph = []
        self.connection = []

        self.mRootService = 0
        self.serviceVector = []
        self.backUpServiceVector = []
        self.allRootService = []
        self.allEndService = []
        self.paths = []
        self.NodeVector = []
        self.SetVector = []
        self.mServiceInfoFromConfVector = []
        self.flag = []
        self.hasFlag = []

        self.results = ResultSet()

    def GetAllInputService(self):
        self.allRootService = []
        for _ in range(len(self.serviceVector)):
            if (len(self.serviceVector[_].parents) == 0):
                self.allRootService.append(self.serviceVector[_])

    def GetAllOutputService(self):
        self.allEndService = []
        for _ in range(len(self.serviceVector)):
            if (len(self.serviceVector[_].children) == 0):
                self.allEndService.append(self.serviceVector[_])

    def splitString(self, str, a):
        temp = str
        mVector = []
        while True:
            index = temp.indexOf(a)
            if (index != -1):
                substr = temp[0:index]
                mVector.append(float(substr))
                temp = temp[:index + 1]
            else:
                mVector.append(float(temp))
                break
        return mVector

    def ReadXMLToGenService(self, config):  # "conf.xml"
        self.mServiceInfoFromConfVector = []
        try:
            dom = xml.dom.minidom.parse(config)
            root = dom.documentElement
            jobList = root.getElementsByTagName("job")
            for _ in range(len(jobList)):
                tempservice = ServiceInfoFromConf()
                tempservice.index = _ + 1
                tempservice.id = jobList[_].getAttribute("id")
                self.mServiceInfoFromConfVector.append(tempservice)
            self.serviceNum = len(jobList)
        except Exception as e:
            print("except:", e)

    def GenService(self):
        self.serviceVector = []
        for _ in range(self.serviceNum):
            tempservice = Service()
            tempservice.index = _ + 1
            for j in range(len(self.mServiceInfoFromConfVector)):
                mtempInfo = self.mServiceInfoFromConfVector[j]
                if (mtempInfo.index == tempservice.index):
                    tempservice.id = mtempInfo.id;
                    tempservice.RT = 0;
                    self.serviceVector.append(tempservice);

    def GetServiceRelation(self, config):
        try:
            dom = xml.dom.minidom.parse(config)
            root = dom.documentElement
            childList = root.getElementsByTagName("child")
            for i in range(len(childList)):
                attributeOfJob = childList[i].getAttribute("ref")
                for j in range(len(self.serviceVector)):
                    if (attributeOfJob == self.serviceVector[j].id):
                        tempChildService = self.serviceVector[j]
                        break
                l = childList[i].getElementsByTagName("parent")  ##########################3todo
                for s in range(len(l)):
                    if (l[s].nodeName == "parent"):
                        attributeOfUses = l[s].getAttribute("ref")
                        for k in range(len(self.serviceVector)):
                            if (attributeOfUses == self.serviceVector[k].id):
                                tempChildService.parents.append(self.serviceVector[k])
                                self.serviceVector[k].children.append(tempChildService)
                                break
        except Exception as e:
            print(e)

    def getAllFiles(self, path, files, file):
        filelist = os.listdir(path)
        for j in range(len(filelist)):
            fileinfo = path + "\\" + filelist[j]
            """if(os.path.isdir(fileinfo)):
                if ("."!=filelist[j] and ".."!=(filelist[j])):
                    files[i] = path+"\\"+filelist[j]
                    file[i] = filelist[j]
                    i=i+1
                    self.getAllFiles(path+"\\"+filelist[j], files, file)
            else:"""
            files.append(path + "\\" + filelist[j])
            file.append(filelist[j])
        # print(files)
        # print(len(files))

    def GetServiceMap(self):
        files = []
        file = []
        filePath = "data\\服务名聚类最终结果"
        self.getAllFiles(filePath, files, file)
        try:
            for i in range(233):
                br = open(files[i])
                index = int(file[i][0:file[i].find(".")])
                tempIntVector = []
                j = 0
                temp = br.readline()
                # print(temp)
                while temp:
                    tempId = int(temp[0:temp.find(":")])
                    # print(tempId)
                    if (tempId != 0):
                        tempIntVector.append(tempId)
                        j = j + 1
                    temp = br.readline()
                self.mServiceMap[index] = tempIntVector
        except Exception as e:
            print(e)
        # print(self.mServiceMap)

    def GenNode(self):
        self.NodeVector = []
        try:
            reader1 = open("data\\QWS_Dataset.txt")
            i = 0
            temp = reader1.readline()
            while (temp):
                # print(temp)
                tempnode = Node()
                tempnode.id = int(temp[0: temp.find(",")])
                temp = temp[temp.find(",") + 1:]
                # print(temp)
                tempDoubleVector = temp.split(",")
                tempnode.responseTime = float(tempDoubleVector[0])
                tempnode.availability = float(tempDoubleVector[1])
                tempnode.throughput = float(tempDoubleVector[2])
                tempnode.successability = float(tempDoubleVector[3])
                tempnode.reliability = float(tempDoubleVector[4])
                # print(tempDoubleVector)
                self.NodeVector.append(tempnode)
                i = i + 1
                if (i == TOTAL_NODE):
                    break
                temp = reader1.readline()
            # print(len(self.NodeVector))
        except Exception as e:
            print(e)

    def GetPrice(self):
        maxTime = 0
        maxAvail = 0
        maxThrou = 0
        maxSuccess = 0
        maxReli = 0
        for i in range(TOTAL_NODE):
            # print(i)
            # print(self.NodeVector)
            if (self.NodeVector[i].responseTime > maxTime):
                maxTime = self.NodeVector[i].responseTime
            if (self.NodeVector[i].availability > maxAvail):
                maxAvail = self.NodeVector[i].availability
            if (self.NodeVector[i].throughput > maxThrou):
                maxThrou = self.NodeVector[i].throughput
            if (self.NodeVector[i].successability > maxSuccess):
                maxSuccess = self.NodeVector[i].successability
            if (self.NodeVector[i].reliability > maxReli):
                maxReli = self.NodeVector[i].reliability
        for i in range(TOTAL_NODE):
            self.NodeVector[i].price = 0.2 * (self.NodeVector[i].responseTime / maxTime) + 0.2 * (
                        self.NodeVector[i].availability / maxAvail) + \
                                       0.2 * (self.NodeVector[i].throughput / maxThrou) + 0.2 * (
                                                   self.NodeVector[i].successability / maxSuccess) + \
                                       0.2 * (self.NodeVector[i].reliability / maxReli)

    def SetBackUpService(self):
        self.backUpServiceVector = []
        for i in range(self.serviceNum):
            temp = Service()
            temp.index = self.serviceVector[i].index
            temp.id = self.serviceVector[i].id
            temp.RT = 0
            for j in range(len(self.serviceVector[i].parents)):
                temp.parents.append(self.serviceVector[i].parents[j])
            for k in range(len(self.serviceVector[i].children)):
                temp.children.append(self.serviceVector[i].children[k])
            self.backUpServiceVector.append(temp)

    def SetNodeSet(self):
        self.nodeSet = []
        # print("!!!!!!!")
        try:
            reader2 = open(self.nodeSet_file,'r')
            tempString = "#{}".format(self.serviceNum)
            temp = reader2.readline()[:-1]
            # print(tempString)
            while (temp):
                if (temp == tempString):
                    temp = reader2.readline()
                    while (True):
                        index = temp.find(" ")
                        if (index != -1):
                            substr = temp[0: index]
                            # print(substr)
                            self.nodeSet.append(int(substr))
                            # print(self.nodeSet)
                            temp = temp[index + 1:]
                        else:
                            self.nodeSet.append(int(temp))
                            # print(self.nodeSet)
                            break
                    break
        except Exception as e:
            print(e)

    def GetGraph(self):
        self.graph = []
        for i in range(self.serviceNum):
            temp = []
            for j in range(self.serviceNum):
                temp.append(0)
            self.graph.append(temp)
        for i in range(self.serviceNum):
            for j in range(len(self.serviceVector[i].children)):
                self.graph[i][self.serviceVector[i].children[j].index - 1] = 1

    def getPaths(self, start, end, sum):
        self.hasFlag[start] = 1
        # print(self.graph)
        # print(self.hasFlag)
        for j in range(self.serviceNum):
            if (self.graph[start][j] == 0 or self.hasFlag[j] == 1):
                continue
            if (j == end):
                self.paths.append(sum + 1)
                continue
            self.getPaths(j, end, sum + 1)
            self.hasFlag[j] = 0

    def Connect(self, start, end):
        self.hasFlag = []
        for i in range(self.serviceNum):
            self.hasFlag.append(0)
        self.paths.clear()
        self.getPaths(start, end, 0)
        if (len(self.paths) == 0):
            return False
        else:
            return True

    def GetConnection(self):
        self.connection = []
        for i in range(self.serviceNum):
            temp = []
            for j in range(self.serviceNum):
                temp.append(0)
            self.connection.append(temp)
        for i in range(self.serviceNum):
            for j in range(self.serviceNum):
                if (i != j):
                    if (self.Connect(i, j)):
                        self.connection[i][j] = 1

    def GenSet(self):
        self.SetVector = []
        for i in range(1, NODE_SET + 1):
            tempset = Set()
            tempset.id = i
            tempset.maxTime = self.NodeVector[self.mServiceMap[i][0] - 1].responseTime
            tempset.minTime = self.NodeVector[self.mServiceMap[i][0] - 1].responseTime
            tempset.maxAvailability = self.NodeVector[self.mServiceMap[i][0] - 1].availability
            tempset.minAvailability = self.NodeVector[self.mServiceMap[i][0] - 1].availability
            tempset.maxPrice = self.NodeVector[self.mServiceMap[i][0] - 1].price
            tempset.minPrice = self.NodeVector[self.mServiceMap[i][0] - 1].price
            tempset.maxReliability = self.NodeVector[self.mServiceMap[i][0] - 1].reliability
            tempset.minReliability = self.NodeVector[self.mServiceMap[i][0] - 1].reliability
            tempset.maxSuccessability = self.NodeVector[self.mServiceMap[i][0] - 1].successability
            tempset.minSuccessability = self.NodeVector[self.mServiceMap[i][0] - 1].successability
            tempset.maxThroughput = self.NodeVector[self.mServiceMap[i][0] - 1].throughput
            tempset.minThroughput = self.NodeVector[self.mServiceMap[i][0] - 1].throughput
            for j in range(len(self.mServiceMap[i])):
                if (self.NodeVector[self.mServiceMap[i][j] - 1].responseTime > tempset.maxTime):
                    tempset.maxTime = self.NodeVector[self.mServiceMap[i][j] - 1].responseTime
                if (self.NodeVector[self.mServiceMap[i][j] - 1].responseTime < tempset.minTime):
                    tempset.minTime = self.NodeVector[self.mServiceMap[i][j] - 1].responseTime
                if (self.NodeVector[self.mServiceMap[i][j] - 1].availability > tempset.maxAvailability):
                    tempset.maxAvailability = self.NodeVector[self.mServiceMap[i][j] - 1].availability
                if (self.NodeVector[self.mServiceMap[i][j] - 1].availability < tempset.minAvailability):
                    tempset.minAvailability = self.NodeVector[self.mServiceMap[i][j] - 1].availability
                if (self.NodeVector[self.mServiceMap[i][j] - 1].price > tempset.maxPrice):
                    tempset.maxPrice = self.NodeVector[self.mServiceMap[i][j] - 1].price
                if (self.NodeVector[self.mServiceMap[i][j] - 1].price < tempset.minPrice):
                    tempset.minPrice = self.NodeVector[self.mServiceMap[i][j] - 1].price
                if (self.NodeVector[self.mServiceMap[i][j] - 1].reliability > tempset.maxReliability):
                    tempset.maxReliability = self.NodeVector[self.mServiceMap[i][j] - 1].reliability
                if (self.NodeVector[self.mServiceMap[i][j] - 1].reliability < tempset.minReliability):
                    tempset.minReliability = self.NodeVector[self.mServiceMap[i][j] - 1].reliability
                if (self.NodeVector[self.mServiceMap[i][j] - 1].successability > tempset.maxSuccessability):
                    tempset.maxSuccessability = self.NodeVector[self.mServiceMap[i][j] - 1].successability
                if (self.NodeVector[self.mServiceMap[i][j] - 1].successability < tempset.minSuccessability):
                    tempset.minSuccessability = self.NodeVector[self.mServiceMap[i][j] - 1].successability
                if (self.NodeVector[self.mServiceMap[i][j] - 1].throughput > tempset.maxThroughput):
                    tempset.maxThroughput = self.NodeVector[self.mServiceMap[i][j] - 1].throughput
                if (self.NodeVector[self.mServiceMap[i][j] - 1].throughput < tempset.minThroughput):
                    tempset.minThroughput = self.NodeVector[self.mServiceMap[i][j] - 1].throughput
            self.SetVector.append(tempset)

    def Init(self, config):
        self.ReadXMLToGenService(config)
        self.GenService()
        self.GetServiceRelation(config)
        self.GetServiceMap()
        self.GenNode()
        self.GetPrice()
        self.SetBackUpService()
        self.GenSet()
        self.SetNodeSet()
        self.GetGraph()
        self.GetConnection()

    def GetBackUpService(self):
        for i in range(self.serviceNum):
            self.serviceVector[i].index = self.backUpServiceVector[i].index
            self.serviceVector[i].id = self.backUpServiceVector[i].id
            self.serviceVector[i].RT = 0

    def GetServiceNode(self, a):
        self.serviceNode = []
        # print(a)
        for i in range(self.serviceNum):
            # print(self.mServiceMap[self.nodeSet[i]])
            self.serviceNode.append(self.mServiceMap[self.nodeSet[i]][a[i]])

    def UpdateInfo(self, a):
        self.GetBackUpService()
        self.GetServiceNode(a)

    def AllServiceCalculate(self):
        j = 0
        for i in range(self.serviceNum):
            if (self.flag[i] != 1):
                break
            j = j + 1
        if (j == self.serviceNum):
            return True
        else:
            return False

    def AllParentsCalculate(self, serviceId):
        j = 0
        for i in range(len(self.serviceVector[serviceId].parents)):
            id = self.serviceVector[serviceId].parents[i].index - 1
            if (self.flag[id] != 1):
                break
            j = j + 1
        if (j == len(self.serviceVector[serviceId].parents)):
            return True
        else:
            return False

    def CalculateResponseTime(self):
        for i in range(self.serviceNum):
            self.flag[i] = 0
        self.GetAllInputService()
        for i in range(len(self.allRootService)):
            id = self.allRootService[i].index - 1
            self.serviceVector[id].RT = self.NodeVector[self.serviceNode[id] - 1].responseTime
            self.flag[id] = 1
        while (not (self.AllServiceCalculate())):
            for i in range(self.serviceNum):
                if (self.flag[i] == 0 and self.AllParentsCalculate(i)):
                    maxTime = 0
                    for j in range(len(self.serviceVector[i].parents)):
                        if (self.serviceVector[i].parents[j].RT > maxTime):
                            maxTime = self.serviceVector[i].parents[j].RT
                    self.serviceVector[i].RT = maxTime + self.NodeVector[self.serviceNode[i] - 1].responseTime
                    self.flag[i] = 1
        self.GetAllOutputService()
        wholeTime = 0
        for i in range(len(self.allEndService)):
            if (self.allEndService[i].RT > wholeTime):
                wholeTime = self.allEndService[i].RT
        return wholeTime

    def CalculateThroughput(self):
        for i in range(self.serviceNum):
            self.flag[i] = 0
        for i in range(self.serviceNum):
            if (self.flag[i] == 0):
                temp = []
                temp.append(i)
                for j in range(self.serviceNum):
                    if (self.serviceNode[j] == self.serviceNode[i] and self.flag[j] == 0):
                        p = 0
                        for k in range(len(temp)):
                            p = p + 1
                            if (self.connection[temp[k]][j] == 1):
                                break
                        if (p == len(temp)):
                            temp.append(j)
                for j in range(len(temp)):
                    self.serviceVector[temp[j]].throughput = self.NodeVector[self.serviceNode[i] - 1].throughput / len(
                        temp)
                    self.flag[temp[j]] = 1
        wholeThroughput = self.serviceVector[0].throughput
        for i in range(self.serviceNum):
            if (self.serviceVector[i].throughput < wholeThroughput):
                wholeThroughput = self.serviceVector[i].throughput
        return wholeThroughput

    def CalculateAvailability(self):
        wholeAvailability = 1
        for i in range(self.serviceNum):
            wholeAvailability = wholeAvailability * self.NodeVector[self.serviceNode[i] - 1].availability / 100
        return wholeAvailability * 100

    def CalculateSuccessability(self):
        wholeSuccessability = 1
        for i in range(self.serviceNum):
            wholeSuccessability = wholeSuccessability * self.NodeVector[self.serviceNode[i] - 1].successability / 100;
        return wholeSuccessability * 100

    def CalculateReliability(self):
        wholeReliability = 1
        for i in range(self.serviceNum):
            wholeReliability = wholeReliability * self.NodeVector[self.serviceNode[i] - 1].reliability / 100
        return wholeReliability * 100

    def CalculateCost(self):
        wholeCost = 0
        for i in range(self.serviceNum):
            wholeCost = wholeCost + self.NodeVector[self.serviceNode[i] - 1].price
        return wholeCost

    def split(selg, str, pattern):
        result = []
        size = len(str)
        for i in range(size):
            pos = str.find(pattern, i)
            if (pos < size):
                s = str[i: pos - i]
                result.append(s)
                i = pos + len(pattern) - 1
        return result

    def Run(self, a):
        self.UpdateInfo(a)
        self.results.time = self.CalculateResponseTime()
        self.results.avail = self.CalculateAvailability()
        self.results.throu = self.CalculateThroughput()
        self.results.success = self.CalculateSuccessability()
        self.results.reli = self.CalculateReliability()
        self.results.cost = self.CalculateCost()
        return self.results

    def calculateMaxTime(self):
        self.flag = []
        for i in range(self.serviceNum):
            self.flag.append(0)
        self.GetAllInputService()
        # print(len(self.nodeSet))
        for i in range(len(self.allRootService)):
            id = self.allRootService[i].index - 1
            self.serviceVector[id].maxRT = self.SetVector[self.nodeSet[id] - 1].maxTime
            self.flag[id] = 1
        while (not self.AllServiceCalculate()):
            for i in range(self.serviceNum):
                if (self.flag[i] == 0 and self.AllParentsCalculate(i)):
                    maxTime = 0
                    for j in range(len(self.serviceVector[i].parents)):
                        if (self.serviceVector[i].parents[j].maxRT > maxTime):
                            maxTime = self.serviceVector[i].parents[j].maxRT
                    self.serviceVector[i].maxRT = maxTime + self.SetVector[self.nodeSet[i] - 1].maxTime
                    self.flag[i] = 1
                # print(self.flag)
        self.GetAllOutputService()
        wholeTime = 0
        for i in range(len(self.allEndService)):
            if (self.allEndService[i].maxRT > wholeTime):
                wholeTime = self.allEndService[i].maxRT
        return wholeTime

    def calculateMinTime(self):
        for i in range(self.serviceNum):
            self.flag[i] = 0
        self.GetAllInputService()
        for i in range(len(self.allRootService)):
            id = self.allRootService[i].index - 1
            self.serviceVector[id].minRT = self.SetVector[self.nodeSet[id] - 1].minTime
            self.flag[id] = 1
        while (not self.AllServiceCalculate()):
            for i in range(self.serviceNum):
                if (self.flag[i] == 0 and self.AllParentsCalculate(i)):
                    maxTime = 0
                    for j in range(len(self.serviceVector[i].parents)):
                        if (self.serviceVector[i].parents[j].minRT > maxTime):
                            maxTime = self.serviceVector[i].parents[j].minRT
                    self.serviceVector[i].minRT = maxTime + self.SetVector[self.nodeSet[i] - 1].minTime
                    self.flag[i] = 1
        self.GetAllOutputService()
        wholeTime = 0
        for i in range(len(self.allEndService)):
            if (self.allEndService[i].minRT > wholeTime):
                wholeTime = self.allEndService[i].minRT
        return wholeTime

    def calculateMaxThrou(self):
        for i in range(self.serviceNum):
            self.flag[i] = 0
        for i in range(self.serviceNum):
            if (self.flag[i] == 0):
                temp = []
                temp.append(i)
                j = i + 1
                for j in range(self.serviceNum):
                    if (self.nodeSet[j] == self.nodeSet[i] and self.flag[j] == 0):
                        p = 0
                        for k in range(len(temp)):
                            p = p + 1
                            if (self.connection[temp[k]][j] == 1):
                                break
                        if (p == len(temp)):
                            temp.append(j)
                for j in range(len(temp)):
                    self.serviceVector[temp[j]].maxThrou = self.SetVector[self.nodeSet[i] - 1].maxThroughput / len(temp)
                    self.flag[temp[j]] = 1
        wholeThroughput = self.serviceVector[0].maxThrou
        for i in range(self.serviceNum):
            if (self.serviceVector[i].maxThrou < wholeThroughput):
                wholeThroughput = self.serviceVector[i].maxThrou
        return wholeThroughput

    def calculateMinThrou(self):
        for i in range(self.serviceNum):
            self.flag[i] = 0
        for i in range(self.serviceNum):
            if (self.flag[i] == 0):
                temp = []
                temp.append(i)
                j = i + 1
                for j in range(self.serviceNum):
                    if (self.nodeSet[j] == self.nodeSet[i] and self.flag[j] == 0):
                        p = 0
                        for k in range(len(temp)):
                            p = p + 1
                            if (self.connection[temp[k]][j] == 1):
                                break
                        if (p == len(temp)):
                            temp.append(j)
                for j in range(len(temp)):
                    self.serviceVector[temp[j]].minThrou = self.SetVector[self.nodeSet[i] - 1].minThroughput / len(temp)
                    self.flag[temp[j]] = 1
        wholeThroughput = self.serviceVector[0].minThrou
        for i in range(self.serviceNum):
            if (self.serviceVector[i].minThrou < wholeThroughput):
                wholeThroughput = self.serviceVector[i].minThrou
        return wholeThroughput

    def calculateMaxAva(self):
        wholeAvailability = 1
        for i in range(self.serviceNum):
            wholeAvailability = wholeAvailability * self.SetVector[self.nodeSet[i] - 1].maxAvailability / 100
        return wholeAvailability * 100

    def calculateMinAva(self):
        wholeAvailability = 1
        for i in range(self.serviceNum):
            wholeAvailability = wholeAvailability * self.SetVector[self.nodeSet[i] - 1].minAvailability / 100
        return wholeAvailability * 100

    def calculateMaxReli(self):
        wholeReliability = 1
        for i in range(self.serviceNum):
            wholeReliability = wholeReliability * self.SetVector[self.nodeSet[i] - 1].maxReliability / 100
        return wholeReliability * 100

    def calculateMinReli(self):
        wholeReliability = 1
        for i in range(self.serviceNum):
            wholeReliability = wholeReliability * self.SetVector[self.nodeSet[i] - 1].minReliability / 100
        return wholeReliability * 100

    def calculateMaxSucc(self):
        wholeSuccessability = 1
        for i in range(self.serviceNum):
            wholeSuccessability = wholeSuccessability * self.SetVector[self.nodeSet[i] - 1].maxSuccessability / 100
        return wholeSuccessability * 100

    def calculateMinSucc(self):
        wholeSuccessability = 1
        for i in range(self.serviceNum):
            wholeSuccessability = wholeSuccessability * self.SetVector[self.nodeSet[i] - 1].minSuccessability / 100
        return wholeSuccessability * 100

    def calculateMaxCost(self):
        wholeCost = 0
        for i in range(self.serviceNum):
            wholeCost = wholeCost + self.SetVector[self.nodeSet[i] - 1].maxPrice
        return wholeCost

    def calculateMinCost(self):
        wholeCost = 0
        for i in range(self.serviceNum):
            wholeCost = wholeCost + self.SetVector[self.nodeSet[i] - 1].minPrice
        return wholeCost

    def obj_eval(self, x_var):
        mArray = []
        for n in range(self.serviceNum):
            mArray.append(x_var[n])
        mResultSet = self.Run(mArray)
        y_obj = []
        y_obj.append(mResultSet.time)
        y_obj.append(mResultSet.cost)
        y_obj.append(mResultSet.avail)
        y_obj.append(mResultSet.reli)
        y_obj.append(mResultSet.success)
        y_obj.append(mResultSet.throu)
        return y_obj

    def receive(self, mArray):
        conf = self.conf_file
        self.Init(conf)
        maxTime = self.calculateMaxTime()
        minTime = self.calculateMinTime()
        maxPrice = self.calculateMaxCost()
        minPrice = self.calculateMinCost()
        maxAvail = self.calculateMaxAva()
        minAvail = self.calculateMinAva()
        maxReli = self.calculateMaxReli()
        minReli = self.calculateMinReli()
        maxSucc = self.calculateMaxSucc()
        minSucc = self.calculateMinSucc()
        maxThrou = self.calculateMaxThrou()
        minThrou = self.calculateMinThrou()
        r = self.obj_eval(mArray)
        f1 = ((r[0] - minTime) / (maxTime - minTime)) + ((r[1] - minPrice) / (maxPrice - minPrice)) + (
                    -(r[2] - minAvail) / (maxAvail - minAvail)) + \
             (-(r[3] - minReli) / (maxReli - minReli)) + (-(r[4] - minSucc) / (maxSucc - minSucc)) + (
                         -(r[5] - minThrou) / (maxThrou - minThrou))
        f = -1.0 / 6 * f1
        return f


if __name__ == "__main__":
    conf_file = "test/10/1/conf.xml"
    nodeSet_file = "test/10/1/nodeSet.txt"
    calattr = Calattr(conf_file, nodeSet_file)
    mArray = [3, 51, 4, 3, 1, 1, 0, 14, 1, 0]
    print(len(mArray))
    f = calattr.receive(mArray)
    print(f)
    print("ok")
