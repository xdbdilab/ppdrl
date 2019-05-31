class SC_DataGenerator(object):
    def __init__(self):
        self.num_service=0
    def init(self,f_path):
        f=open(f_path)
        num_service = []
        f.readline()
        line = f.readline()
        candidates_c = line.split(' ')
        candidates = []
        for index in range(len(candidates_c)):
            candidates.append(candidates_c[index])
        for candidate in candidates:
            num = 0
            f1 = open('服务名聚类最终结果/' + candidate + '.txt')
            line1 = f1.readline()
            while line1:
                num = num + 1
                line1 = f1.readline()
            num_service.append(num)
        self.num_service=num_service
    def get_num_service(self):
        return self.num_service


if __name__ == "__main__":
    pass


