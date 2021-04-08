import numpy as np
import math
#AGNES算法：
#这种算法是从下往上开始聚类
#1.先将所有的点当作一个簇，并且计算出距离矩阵
#2.在距离矩阵中找出最近的俩个距离簇，将之合并，这里直接删除
#3.更新距离矩阵，先删除合并掉的行和列
#4.重新计算合并后的簇与各个簇之间的距离
#5.将簇的个数-1，如果大于K继续循环，否则退出

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


#距离函数，集合间的距离计算常采用豪斯多夫距离
def haoDistance(data_one,data_two):
    #print('data_one',data_one)
    maxOne = np.max(data_one,axis=0)
    minOne = np.min(data_one,axis=0)
    maxTwo = np.max(data_two,axis=0)
    minTwo = np.min(data_two,axis=0)
    #print(maxOne,minTwo)
    tempXToZ = 0
    tempZToX = 0
    m,n = maxOne.shape
    for i in range(n):
        tempXToZ += math.pow(maxOne[:,i] - minTwo[:,i],2)
        #print(tempXToZ)
        tempZToX += math.pow(maxTwo[:,i] - minOne[:,i],2)
    #print(tempXToZ)
    distXToZ = math.sqrt(tempXToZ)
    distZToX = math.sqrt(tempZToX)
    distH = max(distXToZ,distZToX)
    #print('distH',distH)
    return distH
    


#更新簇和距离矩阵
def updateMatAndCluster(minRow,minCol,cluster,distanceMat):
    #print(len(cluster))
    minNum = min(minRow,minCol)
    maxNum = max(minRow,minCol)
    #print(minNum,maxNum)
    #合并簇
    #cluster[minNum] = np.hstack((cluster[minNum],cluster[maxNum]))
    cluster[minNum] = np.row_stack((cluster[minNum],cluster[maxNum]))
    del cluster[maxNum]
    #print(cluster)
    #print(len(cluster))
    
    #更新距离矩阵
    distanceMat = np.delete(distanceMat,maxNum,axis=0)
    distanceMat = np.delete(distanceMat,maxNum,axis=1)
    m,n = distanceMat.shape
    #print(m)
    for i in range(m):
        if i != minNum:
            #print(i)
            distanceNum = haoDistance(cluster[minNum],cluster[i])
            distanceMat[i,minNum] = distanceNum
            distanceMat[minNum,i] = distanceNum
    #print('距离矩阵',distanceMat)
    return distanceMat

#整个函数过程
#k是表示分为多少个簇
def agnesProcess(dataSet,k):
    dataMat = np.mat(dataSet)
    #print(dataMat)
    m,n = dataMat.shape
    cluster = []
    #先把所有的个体单独分成一个簇
    for data in dataMat:
        cluster.append(data)
    #print(cluster)
    #初始距离矩阵
    distanceMat = np.mat(np.zeros((m,m)))
    for i in range(m):
        distanceMat[i,i] = float('inf')
        for j in range(i+1,m):
            #print(dataMat[i],dataMat[j])
            distanceNum = haoDistance(dataMat[i],dataMat[j])   
            #print(distanceNum)
            distanceMat[i,j] = distanceNum
            distanceMat[j,i] = distanceNum
    #print(distanceMat)
    while len(cluster) > k:
        #找出距离最小的俩个簇
        #得出的是扁平化坐标，需要将之展开
        minColAndRow = np.unravel_index(np.argmin(distanceMat),\
                                           distanceMat.shape)
        minRow = minColAndRow[0]
        minCol = minColAndRow[1]
        #更新簇和距离矩阵
        distanceMat = updateMatAndCluster(minRow,minCol,cluster,distanceMat)
        #print(cluster)
    return cluster
        
if __name__ == '__main__':
    dataSet,labelSet = createData()
    cluster = agnesProcess(dataSet,3)
    print(len(cluster))
    
        
        
        
    
