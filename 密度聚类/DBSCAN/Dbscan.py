import random
import copy
import math
#DBSCAN
#聚类结构能够通过样本的紧密程度确定
#1.由给定的限制条件（邻域大小和邻域内的点数量）得出所有的核心对象
#  ，不满足条件的为离群点
#2.对这一组核心对象进行循环处理
#3.随机选择一个核心对象，算出所有的点
#4.使用点数量进行判断是否为核心对象，因为只有核心对象才是出发点
#5.如果是核心对象，将这个核心对象所有的点放入队列中，标记为已访问
#6.之后再查看哪些点是核心对象，再找出点标记为已访问
#7.一直循环下去，直接没有点，那么就是一个簇
#8.核心对象集为空的话，就结束，不然继续下去

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

#距离的计算
def distance(one_point,two_point):
    temp = 0
    for i in range(len(one_point)):
        temp += math.pow(one_point[i] - two_point[i],2)
    return math.sqrt(temp)


#DBSCAN的全过程
#radius是这个核心对象的半径
#minpts是满足核心对象需要包含多少个对象
def DbscanProcess(dataSet,radius,minPts):
    #核心对象
    coreObject = []
    #每个对象的范围内的点
    objectPoint = []
    #查找出所有的核心对象
    for i in range(len(dataSet)):
        points = []
        #print('第%d个元素：'%(i))
        for j in range(len(dataSet)):
            pointDistance = distance(dataSet[i],dataSet[j])
            #print(pointDistance)
            if pointDistance < radius:
                points.append(j)
                
        objectPoint.append(points)
        if len(points) > minPts:
            coreObject.append(i)
    print(coreObject)
    #print(objectPoint)
    #初始化簇的个数和整个簇
    k = 0
    cluster = []
    #初始化未访问的对象
    unvisited = [0 for i in range(len(dataSet))]
    #print(unvisited)
    #将所有的核心对象遍历完就结束
    while len(coreObject) > 0:
        oldUnvisited = copy.deepcopy(unvisited)
        #随机选择一个核心对象
        index = random.randrange(0,len(coreObject))
        #print('随机选择出的:',index)
        #初始化一个队列，记录这个簇访问过的点
        thisCluster = []
        thisCluster.append(coreObject[index])
        #print('取出的:',thisCluster)
        #当列表中没有元素，表示结束
        while len(thisCluster) > 0:
            #取出列表中的元素
            #print('取出的:',thisCluster)
            firstElement = thisCluster[0]
            del thisCluster[0]
            #print(firstElement)
            unvisited[firstElement] = 1
            #找出这个核心对象，所有密度可达的核心对象以及点
            if len(objectPoint[firstElement]) > minPts \
               and (firstElement in coreObject):
                for i in objectPoint[firstElement]:
                    #print(i)
                    if unvisited[i] == 0:
                        thisCluster.append(i)
                        unvisited[i] = 1
                        #print(unvisited)
                #print('first',firstElement)
                coreObject.remove(firstElement)
                #print(coreObject)
        #print('剩下的核心对象:',coreObject)
        #这些访问过的点成为一个簇
        k += 1
        temp = []
        print(unvisited)
        for i in range(len(oldUnvisited)):
            if oldUnvisited[i] != unvisited[i]:
                temp.append(i)
        cluster.append(temp)
        #print('簇：',cluster)
    return cluster,k


if __name__ == '__main__':
    dataSet,labels = createData()
    radius = 0.11
    minPts = 4
    cluster,k = DbscanProcess(dataSet,radius,minPts)
    print('分成的簇为,',cluster)
    
        
                    
        
            
             
                
        
