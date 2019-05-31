# coding = utf-8


# 计算给定的nodeSet.txt中一共包含的原子服务总个数
def cal_num(nodeSet_file):
    cluster_files = "data/服务名聚类最终结果"
    fd = open(nodeSet_file, 'r')
    nodeSets = fd.readlines()[1]  # str
    nodeSets = nodeSets.split(' ')  # list
    # print(nodeSets)
    if nodeSets[-1] == '':
        nodeSets = nodeSets[:-1]

    each_services_nums = []
    for node in nodeSets:
        f2 = open(cluster_files + '/' + str(node) + '.txt', 'r')
        atom_nodes = []
        lines = f2.readlines()
        for line in lines:
            atom_node = line.strip('\r\n').split(':')[0]
            atom_nodes.append(int(atom_node))
        each_services_nums.append(len(atom_nodes))
    all_services_nums = sum(each_services_nums)
    nodes_num = len(each_services_nums)
    max_services_num = max(each_services_nums)
    return nodes_num, each_services_nums, all_services_nums, max_services_num


if __name__ == '__main__':
    nodeSet_file = "test/10/2/nodeSet.txt"
    nodes_num, each_services_nums, all_services_nums, max_services_num = cal_num(nodeSet_file)
    print("1.服务节点数：{}".format(nodes_num))
    print("2.每个节点处候选子集大小：{}".format(each_services_nums))
    print("3.总的候选原子个数：{}".format(all_services_nums))
    print("4.最大候选子集个数：{}".format(max_services_num))

