import numpy as np
import math
import copy
#DIANA
#采用是自顶向下的层次聚类，也就是分裂层次聚类
#1.所有的对象放在一个簇中
#2.找出簇直径最大的那个簇，这个就是我们分裂的簇
#3.在这个簇中计算所有点的平均相异度，将平均相异度最大的那个点放在上步生成的簇中
#4.然后开始将old簇中的各个点进行比较，如果到新簇最近点距离小于等于旧簇的最近点
#  的距离，那么将这个点放到新簇中
#5.重复进行第四步，直到没有点满足条件
#6.如果簇的数量大于等于k，那么退出，不然继续

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
##        [0.556, 0.215],
##        # 6
##        [0.403, 0.237],
##        # 7
##        [0.481, 0.149],
##        # 8
##        [0.437, 0.211],
##        # 9
##        [0.666, 0.091],
##        # 10
##        [0.243, 0.267],
##        # 11
##        [0.245, 0.057],
##        # 12
##        [0.343, 0.099],
##        # 13
##        [0.639, 0.161],
##        # 14
##        [0.657, 0.198],
##        # 15
##        [0.360, 0.370],
##        # 16
##        [0.593, 0.042],
##        # 17
##        [0.719, 0.103],
##        # 18
##        [0.359, 0.188],
##        # 19
##        [0.339, 0.241],
##        # 20
##        [0.282, 0.257],
##        # 21
##        [0.748, 0.232],
##        # 22
##        [0.714, 0.346],
##        # 23
##        [0.483, 0.312],
##        # 24
##        [0.478, 0.437],
##        # 25
##        [0.525, 0.369],
##        # 26
##        [0.751, 0.489],
##        # 27
        [0.532, 0.472],
##        # 28
        [0.473, 0.376],
##        # 29
        [0.725, 0.445],
        # 30
        [0.446, 0.459]
    ]

    # 特征值列表

    labels = ['密度', '含糖率']
    return dataSet,labels

#计算距离
def distance(onePoint,twoPoint):
    temp = 0
    for i in range(len(onePoint)):
        temp += math.pow(onePoint[i] - twoPoint[i],2)
    return math.sqrt(temp)

#寻找出直径最大的那个簇
def searchMaxCluster(cluster):
    if len(cluster) == 1:
        return cluster[0]
    else:
        diameterCluster = [0 for i in range(len(cluster))]
        #查看所有簇直径情况
        for num in range(len(cluster)):
            #计算一个簇中所有的点,最长的距离为直径
            diameter = 0
            for i in range(len(cluster[num])):
                for j in range(i,len(cluster[num])):
                    pointDistance = distance(cluster[num][i],cluster[num][j])
                    if pointDistance >= diameter:
                        diameter = pointDistance
            diameterCluster[num] = diameter
        print('所有簇的直径:',diameterCluster)
        #print('需要切分的簇:',cluster[diameterCluster.index(max(diameterCluster))])
        return cluster[diameterCluster.index(max(diameterCluster))]

#找出平均相异点最大的那个
def maxAverDifferent(oldPart):
    averDifferent = []
    maxAverDifferent = 0
    index = 0
    for i in range(len(oldPart)):
        temp = 0
        for j in range(0,len(oldPart)):
            if i != j:
                pointDistance = distance(oldPart[i],oldPart[j])
                temp += pointDistance
        temp = temp / (len(oldPart)-1)
        print(temp)
        if temp > maxAverDifferent:
            maxAverDifferent = temp
            index = i
    print('maxAver:',maxAverDifferent)
    averDifferent = copy.deepcopy(oldPart[index])
    del oldPart[index]
    return averDifferent

#找到其他满足条件的点
def searchPoint(point,num,new,oldPart):
    #计算与old簇最近的点的距离
    minOld = float('inf')
    minNew = float('inf')
    for i in range(len(oldPart)):
        if i != num:
            temp = distance(point,oldPart[i])
            if temp < minOld:
                minOld = temp
    for i in range(len(new)):
        temp = distance(point,new[i])
        if temp < minNew:
            minNew = temp
    cpoyPoint = copy.deepcopy(point)
    print('%d点---->'%(num))
    print('到old的距离',minOld)
    print('到new的距离',minNew)
    print('---------------------')
    if minNew <= minOld:
        new.append(cpoyPoint)
        del oldPart[oldPart.index(point)]
    

#diana算法过程
def DianaProcess(dataSet,k):
    cluster = []
    #先将所有点放在一个簇中
    cluster.append(dataSet)
    while len(cluster) < k:
        #找出直径最大的那个簇
        oldPart = searchMaxCluster(cluster)
        #新簇
        new = []
        #寻找到平均相异度最大的那个点
        averDifferent = maxAverDifferent(oldPart)
        new.append(averDifferent)
        #print('增加平均相异度最大的点:',new)
        #开始寻找其他的点
        copyOldPart = copy.deepcopy(oldPart)
        if len(copyOldPart) > 1:
            #print('寻找其他的点')
            for i in range(len(copyOldPart)):      
                #print(i,len(oldPart),oldPart)
              
                searchPoint(copyOldPart[i],i,new,oldPart)     
        cluster.append(new)
        #print('分出的簇：',cluster)
        #print('=======================')
    return cluster


if __name__ == '__main__':
    dataSet,labelSet = createData()
    cluster = DianaProcess(dataSet,2)
    for i in range(len(cluster)):
        print('第%d个簇：%s' % (i,cluster[i]))
