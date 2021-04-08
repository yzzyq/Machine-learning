import dataSetExract as extract
import numpy as np
import math
#K-均值算法
#1.随机选择K个簇心
#2.将每个数据依次和每个簇心进行欧式距离计算
#3.找出最近簇心，分配到最新簇心中
#4.利用均值重新计算k个簇心
#5.当所有的数据都不在重新分配簇心，那么完成

#距离公式
def getDistance(dataSet,clusterCenter):
    sumData = 0
    clusterCenter = clusterCenter[0]
    for i in range(len(dataSet)):
        temp = math.pow(dataSet[i] - clusterCenter[i],2)
        sumData += temp
    return math.sqrt(sumData)


#创建k个簇心
#簇心的值在整个数据的范围之内
def createCenter(k,dataSet):
    cols = np.shape(dataSet[:])[1]
    clusterCenter = np.mat(np.zeros((k,cols)))
    dataSet = np.mat(dataSet)
    #为k个簇心的每一列赋初值
    for i in range(cols):
        #随机值必须在范围之内
        minCol = min(dataSet[:,i])
        dataSet.astype('float64')
        rangeCol = float(max(dataSet[:,i]) - minCol)
        clusterCenter[:,i] = minCol + rangeCol*np.random.rand(k,1)
    return clusterCenter
    


#k均值算法
#disMehtod 距离计算方法
#crateCenter 创建k个簇心
#返回所有的簇心和点分配结果
def KMeans(dataSet,k,disMethod,createCenter):
    rows = len(dataSet)
    #每个点分配簇心情况，第一列就是分配到的簇心，第二列就是距离
    clusterAssment = np.zeros((rows,2))
    #创建k个簇心
    clusterCenter = createCenter(k,dataSet)
    clusterChange = True
    #如果簇心都不改变了，那么可以退出了
    while clusterChange:
        clusterChange = False
        #对每个点进行遍历计算簇
        for i in range(rows):
            minDistance = np.inf
            minIndex = -1
            #计算这个点与所有簇心的距离
            for j in range(k):
                #计算每个点和一个簇心的距离
                distance = disMethod(dataSet[i],clusterCenter[j].tolist())
                if distance < minDistance:
                    minDistance = distance
                    minIndex = j
            #判断是否需要更新这个点的簇心
            if clusterAssment[i][0] != minIndex:
                clusterChange = True
            clusterAssment[i][0] = minIndex
            clusterAssment[i][1] = minDistance
            if clusterChange:
                #簇心发生了变化，就需要更新簇心
                #求所有簇的平均值作为簇心
                for num in range(k):
                    allPoint = []
                    #找出属于这个簇心的所有的点
                    for a in range(len(clusterAssment)):
                        if clusterAssment[a][0] == num:
                            allPoint.append(dataSet[a])
                    #利用均值计算出新的簇心
                    clusterCenter[num] = np.mean(allPoint,axis=0)
    return clusterCenter,clusterAssment


#取出数据
dataSet,labelSet = extract.extractData()
#簇中的个数
k = 2

clusterCenter,clusterAssment = KMeans(dataSet,k,getDistance,createCenter)
print(clusterCenter)
print('========================')
print(clusterAssment)
