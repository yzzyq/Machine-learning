import ClusteringFeature
import globalVar as gl
#叶子结点的簇
class Cluster(ClusteringFeature.ClusterFeatures):

    def __init__(self,dataRecords):
        super().__init__(self)
        #集群中的数据点 
        self.data = []
        #父节点
        self.parentNode = None
        self.data.append(dataRecords)
        
        self.N = len(dataRecords)
        self.setLS(dataRecords) 
        self.setSS(dataRecords)

    def addPoint(self,cluster):
        for i in range(len(cluster.data)):
            temp = cluster.data[i]
            self.data.append(temp)
            self.addCF(cluster)

if __name__ == '__main__':
    cluster = Cluster([[1,2],[3,4]],4)
    print(cluster.data)
        
        
