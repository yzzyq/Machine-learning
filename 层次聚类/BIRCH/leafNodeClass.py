import ClusteringFeature
import copy
import noLeafNodeClass as nlNode
import globalVar as gl

#叶子结点
class leafNode(ClusteringFeature.ClusterFeatures):
    def __init__(self):
        super().__init__(self)
        self.clusterChilds = []
        self.parentNode = None

    #叶子结点中添加集群
    def addCluster(self,cluster):
        #更新聚类特征值
        #父结点也要更新CF
        self.updateClusterFeature(cluster)
        #找出最近的集群点放入
        findCluster = None
        #是否需要分裂
        needDivided = False
        
        if len(self.clusterChilds) == 0:
            #这个叶子结点没有集群，直接放入
            self.clusterChilds.append(cluster)
            cluster.parentNode = self
        else:
            distance = float('inf')
            for c in self.clusterChilds:
                clusterDistance = c.computerClusterDistance(cluster)
                if distance > clusterDistance:
                    distance = clusterDistance
                    findCluster = c
            #找出最近的簇之后，查看簇间距离是否大于阈值了，如果大于阈值，分裂簇
            dataCopy = copy.deepcopy(findCluster.data)
            #print(dataCopy)
            dataCopy.append(cluster.data[0])
            #print(dataCopy)
            #添加数据后的簇直径超过了阈值的话，需要分裂
            #print('添加数据后的簇直径，',findCluster.computerInCluster(dataCopy))
            if findCluster.computerInCluster(dataCopy) > \
               gl.getValue('threshold'):
                #叶子结点的集群数不能超过
                if len(self.clusterChilds) + 1 > gl.getValue('leafBalance'):
                    needDivided = True
                self.clusterChilds.append(cluster)
                cluster.parentNode = self
            else:
                #print('加点前的簇，',findCluster.data)
                findCluster.addPoint(cluster)
                #print('加点后的簇，',findCluster.data)
                cluster.parentNode = self
        if needDivided:
            #结点分裂前的处理
            if self.parentNode == None:
                self.parentNode = nlNode.NoLeafNode()
            else:
                #父结点先要去除这个结点
                self.parentNode.leafChilds.remove(self)
            #分裂后的结点
            leafNodeArray_one,leafNodeArray_two = self.divideLeafNode()
            #print(leafNodeArray_one,leafNodeArray_two)
            self.parentNode.addNode(leafNodeArray_one)
            self.parentNode.addNode(leafNodeArray_two)

    #将叶子结点分为俩个
    def divideLeafNode(self):
        #找出来的差距最大的俩个簇，后面的簇就近原则划分
        cluster_one = None
        cluster_two = None
        #最大的距离
        maxDistance = 0

        #找出俩个差距最大的俩个簇
        for i in range(len(self.clusterChilds)):

            for j in range(i+1,len(self.clusterChilds)):
                distance = self.clusterChilds[i].\
                           computerClusterDistance(self.clusterChilds[j])
                if distance > maxDistance:
                    maxDistance = distance
                    cluster_one = self.clusterChilds[i]
                    cluster_two = self.clusterChilds[j]
        #生成俩个叶子结点
        leafNodeArray_one = leafNode()
        leafNodeArray_one.addCluster(cluster_one)
        cluster_one.parentNode = leafNodeArray_one
        
        leafNodeArray_two = leafNode()
        leafNodeArray_two.addCluster(cluster_two)
        cluster_two.parentNode = leafNodeArray_two

        #去除这俩个集群
        self.clusterChilds.remove(cluster_one)
        self.clusterChilds.remove(cluster_two)
        #就近分配簇
        for c in self.clusterChilds:
            if cluster_one.computerClusterDistance(c) < cluster_two.\
               computerClusterDistance(c):
                #接近哪个就加入哪个
                leafNodeArray_one.addCluster(c)
                c.parentNode = leafNodeArray_one
            else:
                leafNodeArray_two.addCluster(c)
                c.parentNode = leafNodeArray_two
        return leafNodeArray_one,leafNodeArray_two
                
        

    def updateClusterFeature(self,clusterFeature):
        if self.parentNode != None:
            self.parentNode.updateClusterFeature(clusterFeature)
        self.addCF(clusterFeature)



    
    
