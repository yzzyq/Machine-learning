import ClusteringFeature
import leafNodeClass
import globalVar as gl
#非叶子结点
class NoLeafNode(ClusteringFeature.ClusterFeatures):

    def __init__(self):
        super().__init__(self)
        #子结点可能是叶子结点也有可能不是叶子结点，叶子结点是双向链表的形式
        self.nonLeafChilds = None
        self.leafChilds = None
        #父结点
        self.parentNode = None

    #非叶子结点增加子结点，分为增加非叶子结点和叶子结点 
    def addNode(self,node):
        leafNodeNow = None
        noLeafNodeNow = None

        #更新CF
        self.updateClusterFeature(node)

        if isinstance(node,leafNodeClass.leafNode):
            leafNodeNow = node
        else:
            noLeafNodeNow = node

        if leafNodeNow != None:
            #加入后是否需要分裂
            needDivide = self.addingNeedDivide(leafNodeNow)
            if needDivide:
                if self.parentNode == None:
                    self.parentNode = NoLeafNode()
                else:
                    self.parentNode.nonLeafChilds.remove(self)
                leafNode_one,leafNode_two = self.leafNodeDivide()
                self.parentNode.addNode(leafNode_one)
                self.parentNode.addNode(leafNode_two)
        else:
            #加入后是否需要分裂
            needDivide = self.addingNeedDivide(noLeafNodeNow)

            if needDivide:
                if self.parentNode == None:
                    self.parentNode = NoLeafNode()
                else:
                    self.parentNode.nonLeafChilds.remove(self)
                leafNode_one,leafNode_two = self.noLeafNodeDivide()
                self.parentNode.addNode(leafNode_one)
                self.parentNode.addNode(leafNode_two)

    #加入后是否需要分裂
    def addingNeedDivide(self,node):
        needDivide = False
        if isinstance(node,leafNodeClass.leafNode):
            #叶子结点的加入
            if self.leafChilds == None:
                self.leafChilds = []
                self.leafChilds.append(node)
                node.parentNode = self
            else:
                if len(self.leafChilds) + 1 > gl.getValue('leafBalance'):
                    needDivide = True
                self.leafChilds.append(node)
                node.parentNode = self
        else:
            #非叶子结点的加入
            if self.nonLeafChilds == None:
                self.nonLeafChilds = []
                self.nonLeafChilds.append(node)
                node.parentNode = self
            else:
                if len(self.nonLeafChilds) + 1 > gl.getValue('branchBalance'):
                    needDivide = True
                self.nonLeafChilds.append(node)
                node.parentNode = self
        return needDivide
        

    #叶子结点分裂 
    def leafNodeDivide(self):
        #找出来的差距最大的俩个簇，后面的簇就近原则划分
        leaf_one = None
        leaf_two = None
        #最大的距离
        maxDistance = 0

        #找出俩个差距最大的俩个簇
        for i in range(len(self.leafChilds)):

            for j in range(i+1,len(self.leafChilds)):
                distance = self.leafChilds[i].\
                           computerClusterDistance(self.leafChilds[j])
                if distance > maxDistance:
                    maxDistance = distance
                    leaf_one = self.leafChilds[i]
                    leaf_two = self.leafChilds[j]
        #生成俩个叶子结点
        noLeafNodeArray_one = NoLeafNode()
        noLeafNodeArray_one.addNode(leaf_one)
        leaf_one.parentNode = noLeafNodeArray_one
        
        noLeafNodeArray_two = NoLeafNode()
        noLeafNodeArray_two.addNode(leaf_two)
        leaf_two.parentNode = noLeafNodeArray_two

        #去除这俩个集群
        self.leafChilds.remove(leaf_one)
        self.leafChilds.remove(leaf_two)
        #就近分配簇
        for c in self.leafChilds:
            if leaf_one.computerClusterDistance(c) < leaf_two.\
               computerClusterDistance(c):
                #接近哪个就加入哪个
                noLeafNodeArray_one.addNode(c)
                c.parentNode = noLeafNodeArray_one
            else:
                noLeafNodeArray_two.addNode(c)
                c.parentNode = noLeafNodeArray_two
        return noLeafNodeArray_one,noLeafNodeArray_two
        
        
    #非叶子结点分裂
    def noLeafNodeDivide(self):
        #找出来的差距最大的俩个簇，后面的簇就近原则划分
        leaf_one = None
        leaf_two = None
        #最大的距离
        maxDistance = 0
        #找出俩个差距最大的俩个簇
        for i in range(len(self.nonLeafChilds)):

            for j in range(i+1,len(self.nonLeafChilds)):
                distance = self.nonLeafChilds[i].\
                           computerClusterDistance(self.nonLeafChilds[j])
                if distance > maxDistance:
                    maxDistance = distance
                    leaf_one = self.nonLeafChilds[i]
                    leaf_two = self.nonLeafChilds[j]
        #生成俩个非叶子结点
        leafNodeArray_one = NoLeafNode()
        leafNodeArray_one.addNode(leaf_one)
        leaf_one.parentNode = leafNodeArray_one
        
        leafNodeArray_two = NoLeafNode()
        leafNodeArray_two.addNode(leaf_two)
        leaf_two.parentNode = leafNodeArray_two

        #去除这俩个集群
        self.nonLeafChilds.remove(leaf_one)
        self.nonLeafChilds.remove(leaf_two)
        #就近分配簇
        for c in self.nonLeafChilds:
            if leaf_one.computerClusterDistance(c) < leaf_two.\
               computerClusterDistance(c):
                #接近哪个就加入哪个
                leafNodeArray_one.addNode(c)
                c.parentNode = leafNodeArray_one
            else:
                leafNodeArray_two.addNode(c)
                c.parentNode = leafNodeArray_two
        return leafNodeArray_one,leafNodeArray_two

    #寻找到最接近的叶子结点
    def findCloseLeafNode(self,dataCluster):
        #使用递归，这里递归停止的条件就是找到了叶子结点
        leafNodeTemp = None
        nonLeafNodeTemp = None
        minDistance = float('inf')

        #判断递归结束的条件
        if self.nonLeafChilds == None:
            for n in self.leafChilds:
                temp = n.computerClusterDistance(dataCluster)
                if temp < minDistance:
                    minDistance = temp
                    leafNodeTemp = n
        else:
            for n in self.nonLeafChilds:
                temp = n.computerClusterDistance(dataCluster)
                if temp < minDistance:
                    mindistance = temp
                    nonLeafNodeTemp = n

            #递归寻找
            leafNodeTemp = nonLeafNodeTemp.findCloseLeafNode(dataCluster)

        return leafNodeTemp
            
            


    def updateClusterFeature(self,clusterFeature):
        if self.parentNode != None:
            self.parentNode.updateClusterFeature(clusterFeature)
        self.addCF(clusterFeature)
        
        

    
        

