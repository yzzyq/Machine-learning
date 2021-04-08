import ClusterClass
import noLeafNodeClass
import leafNodeClass
import globalVar as gl
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

#BIRCH算法
#就是建立CF树，CF就是类簇总体信息三元组（N,LS,SS）
#数据结构：叶子结点，非叶子结点
#          叶子结点：parentNode,CF,clusterChild(放结点的集群)
#          非叶子结点：CF，child，parentNode
#1.初始化枝平衡因子、叶平衡因子、空间阈值，
#  依次迭代所有的数据来建立一棵CF树
#2.先初始化一个叶子结点，将一个数据放入一个cluster中，将这个cluster加入叶子结点 
#3.在加入叶子结点的时候，先更新CF，然后选出这个叶子结点中最近的簇，
#  如果加入后，这个簇的距离超过了空间阈值，那么在叶子结点下重新建立一个簇
#  之后查看簇的个数是否超过了叶平衡因子
#4.如果超过了叶平衡因子，那么对这个叶子结点进行分裂
#5.分裂之后初始化的父结点成为根结点
#6.在有了根结点后，在一个数据想要插入到树中，必须先找到最近的目标叶子结点
#7.找到了最近的叶子结点，加入叶子结点后，查看是否超过了叶平衡因子
#8.如果超过了叶平衡因子，分裂，查看父结点是否需要分裂
#9.直到所有的数据都遍历完，就完成了CF树的创建


#数据集
def createData():
    dataSet = [
        # 1
        [0.697, 0.460],
        # 2
        [0.774, 0.376],
        # 3
        [0.634, 0.264],
        # 4
        [0.608, 0.318],
        # 5
        [0.556, 0.215],
        # 6
        [0.403, 0.237],
        # 7
        [0.481, 0.149],
        # 8
        [0.437, 0.211],
        # 9
        [0.666, 0.091],
        # 10
        [0.243, 0.267],
        # 11
        [0.245, 0.057],
        # 12
        [0.343, 0.099],
        # 13
        [0.639, 0.161],
        # 14
        [0.657, 0.198],
        # 15
        [0.360, 0.370],
        # 16
        [0.593, 0.042],
        # 17
        [0.719, 0.103],
        # 18
        [0.359, 0.188],
        # 19
        [0.339, 0.241],
        # 20
        [0.282, 0.257],
        # 21
        [0.748, 0.232],
        # 22
        [0.714, 0.346],
        # 23
        [0.483, 0.312],
        # 24
        [0.478, 0.437],
        # 25
        [0.525, 0.369],
        # 26
        [0.751, 0.489],
        # 27
        [0.532, 0.472],
        # 28
        [0.473, 0.376],
        # 29
        [0.725, 0.445],
        # 30
        [0.446, 0.459]
    ]

    # 特征值列表

    labels = ['密度', '含糖率']
    return dataSet,labels

#平衡因子、叶平衡因子、空间阈值
def CrateCFTree(dataSet,branchBalance,leafBalance,threshold):
    #将平衡因子、叶平衡因子、空间阈值设为跨文件全局变量
    gl.init()
    gl.setValue('branchBalance',branchBalance)
    gl.setValue('leafBalance',leafBalance)
    gl.setValue('threshold',threshold)
    
    rootNode = None
    leaf  = None
    cluster = None
    i = 1
 
    #遍历每个数据
    for data in dataSet:
        dataCluster = ClusterClass.Cluster(data)
        #根结点还没有被赋值，根结点是在叶子结点分裂的时候赋值
        if rootNode == None:
            if leaf == None:
                leaf = leafNodeClass.leafNode()
            #将数据加入到叶子结点中去
            leaf.addCluster(dataCluster)
            #print(leaf.LS)
            if leaf.parentNode != None:
                rootNode = leaf.parentNode
        else:
            if rootNode.parentNode != None:
                rootNode = rootNode.parentNode
            findLeaf = rootNode.findCloseLeafNode(dataCluster)
            #print('findLeaf',findLeaf.clusterChilds)
            findLeaf.addCluster(dataCluster)
            #print('====================')
        i += 1
        
    node = leaf.parentNode
    if node == None:
        return leaf
    #print(leaf)
    upNode = node.parentNode
    if upNode == None:
        return node
    else:
        while upNode.parentNode != None:
            upNode = upNode.parentNode
        return upNode


#显示出树
def printTree(node):
    childNode = []
    childNode.append(node)
    clusterAll = []
    #print('显示树')
    while len(childNode) > 0:
        cf = childNode[0]
        del childNode[0]
        if isinstance(cf,leafNodeClass.leafNode):
            for cluster in cf.clusterChilds:
                #print('===================')
                temp = []
                for i in cluster.data:
                    #print(i)
                    temp.append(i)
                clusterAll.append(temp)
                #print('===================')
                #print('cluster:',cluster.data)
        elif isinstance(cf,noLeafNodeClass.NoLeafNode):
            if cf.nonLeafChilds != None:
                for child in cf.nonLeafChilds:
                    childNode.append(child)
            if cf.leafChilds != None:
                for child in cf.leafChilds:
                    childNode.append(child)
    print(len(clusterAll))
    return clusterAll

def Visualization(clusterAll):
    colors = ['b','y','r','k','c','m','g','#e24fff','#524C90','#845868']
    for i in range(len(clusterAll)):
        X = []
        Y = []
        tsne = TSNE(n_components = 2,init = 'pca',random_state = 0)
        if len(clusterAll[i]) > 2:
            result = tsne.fit_transform(clusterAll[i])
            print(result)
            for j in range(len(result)):
                X.append(result[j][0])
                Y.append(result[j,1])
            plt.scatter(X,Y,s=15,c=colors[i])
    plt.xlim(-6000,6000)
    plt.xticks(())
    plt.ylim(-6000,6000)
    plt.yticks(())
    plt.show()

def Visualization(clusterAll):
    colors = ['b','y','r','k','c','m','g','#e24fff','#524C90','#845868']
    for i in range(len(clusterAll)):
        X = []
        Y = []
        result = clusterAll[i]
        for j in range(len(result)):
            X.append(result[j][0])
            Y.append(result[j][1])
        plt.scatter(X,Y,s=15,c=colors[i])
    plt.title('birch')
    plt.xlim(-6000,6000)
    plt.xticks(())
    plt.ylim(-6000,6000)
    plt.yticks(())
    plt.show()
        
    
            
if __name__ == '__main__':
    dataSet,labels = createData()
    print(dataSet)
    node = CrateCFTree(dataSet,3,3,0.4)
    print('==================')
    cluster = printTree(node)
    print(cluster)
    Visualization(cluster)


