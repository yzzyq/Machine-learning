import math
#CF
#聚类特征，所有的结点都有这个类
class ClusterFeatures:
    def __init__(self,N = 0,LS = None,SS = None):
        self.N = N
        self.LS = LS
        self.SS = SS

    #设置LS
    def setLS(self,dataRecords):
        lengthData = len(dataRecords)
        self.LS = [0 for i in range(lengthData)]
        for i in range(lengthData):
            self.LS[i] += dataRecords[i]
        
    #设置SS
    def setSS(self,dataRecords):
        self.SS = [0 for i in range(len(dataRecords))]
        for i in range(len(dataRecords)):
            self.SS[i] += math.pow(dataRecords[i],2)

    #CF向量的叠加
    def addCF(self,otherCF):
        #如果没有需要创建 
        if self.LS == None:
            self.N = 0
            self.LS = [0 for i in range(len(otherCF.LS))]
            self.SS = [0 for i in range(len(otherCF.SS))]
        #俩个CF相加
        for i in range(len(otherCF.LS)):
            self.LS[i] += otherCF.LS[i]
            self.SS[i] += otherCF.SS[i]
        self.N += otherCF.N

    #俩簇之间的度量是使用的CF里面的量
    def computerClusterDistance(self,cluster):
        distance = 0 
        for i in range(len(cluster.LS)):
            distance += math.pow(self.LS[i]/self.N - cluster.LS[i]/cluster.N,2)
        return math.sqrt(distance)

    #簇直径，用于查看加入数据后的簇是否满足阈值，是否需要分裂
    def computerInCluster(self,dataRecords):
        sumDistance = 0
        num = len(dataRecords)
        for i in range(len(dataRecords)-1):
            for j in range(i+1,len(dataRecords)):
                sumDistance += self.computerOuDistance(\
                    dataRecords[i],dataRecords[j])
        return math.sqrt(sumDistance/(num*(num-1)/2))


    #计算俩个点的欧式距离
    def computerOuDistance(self,data_one,data_two):
        distance = 0
        
        for i in range(len(data_one)):
            distance += math.pow(data_one[i] - data_two[i],2)
        return math.sqrt(distance)

if __name__ == '__main__':
    cf = ClusterFeatures()
    print(cf.N)
    cf.setLS([[1,2],[3,4],[5,6]])
    print(cf.LS)
    cf.setSS([[1,2],[3,4],[5,6]])
    print(cf.SS)

    

    
        
        
        
        
