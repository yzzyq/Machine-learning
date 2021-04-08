import copy
import random
import math
#optics
#为了克服DBSCAN输入参数的缺点
#这个算法难点在于核心点的直接可达点的有序列表
#需要输入的就是E和MinPts，在这个算法的E和MinPts只是起辅助作用，也就是他们俩的
#变化并不会应影响到样本点的相对输出顺序，对结果是没有任何影响
#1.找出所有的核心对象，并且创建顺序队列和结果队列，顺序队列存储的是未处理但是
#  即将处理的数据点，结果队列是已经处理过的数据点，结果队列应该是点和可达距离
#2.从数据集dataSet中找出一个不在结果队列并且是核心对象，放入结果队列中，并且
#  进行拓展（找出所有的直接密度可达样本点），把不存在结果队列的样本点放入顺序
#  队列中，并且按照可达距离排序
#3.如果顺序队列中没有点，继续从dataSet中取出核心对象。从顺序队列中取出一个点
#  这个点就是最小可达距离点，放入结果队列，
#  如果这个点不是核心点，那么再从队列中取出一个样本点
#  如果这个点是核心点，那么继续往下处理
#4.拓展这个核心点，找出所有的密度直达样本点，对这些样本点进行判断
#  1.样本点存在于结果队列，那么不处理
#  2.样本点存在顺序队列，并且新的可达距离小于旧的，那么用取代旧的，重新排序
#  3.如果都不存在，直接插入，重新排序
#5.依此进行处理，直到所有的样本点处理完，输出结果队列


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

#计算每个核心对象的核心距离
def computeCoreDistance(index,objectPoint,minPts,dataSet):
    pointDistances = []
    for i in objectPoint[index]:
        pointDistance = distance(dataSet[index],dataSet[i])
        pointDistances.append(pointDistance)
    pointDistances.sort()
    #print('核心距离的选择',pointDistances)
    return pointDistances[minPts]
    
#计算每个元素的可达距离
def computeReachableDistance(point,coreObject,dataSet,coreDistance):
    pointDistance = distance(dataSet[point],dataSet[coreObject])
    #print('点的距离:',pointDistance)
    #print('核心距离：',coreDistance)
    return max(pointDistance,coreDistance)

#样本点是否存在队列中
def isExistList(point,objectList,listIndex):
    isExist = False
    #print('要查找的点，',point)
    #print(objectList)
    for i in range(len(objectList)):
        if objectList[i][0] == point:
            #print(objectList[i][0])
            #print(point)
            #print(i)
            listIndex.append(i)
            isExist = True
            break
    #print('index',index)
    #print('==========')
    return isExist
            

#对顺序队列进行排序    
def sortOrder(orderList):
    for i in range(len(orderList)-1):
        for j in range(len(orderList)-i-1):
            if orderList[j][1] > orderList[j+1][1]:
                orderList[j],orderList[j+1] = orderList[j+1],orderList[j]
    return orderList

#删除核心对象中相应的元素列表
def delete(coreObject,firstElement):
    for i in range(len(coreObject)):
        #print(i)
        if coreObject[i][0] == firstElement:
            del coreObject[i]
            break
    return coreObject
            
def searchIndex(firstElement,coreObject):
    index = 0
    for i in range(len(coreObject)):
        if coreObject[i][0] == firstElement:
            index = i
            break
    return index

def opticsProcess(dataSet,radius,minPts):
    #核心对象和它的核心距离
    coreObject = []
    #顺序队列
    orderList = []
    #结果队列
    resultList = []
    #每个对象的范围内的点
    objectPoint = []
    #找出所有的核心对象
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
    #计算所有核心对象的核心距离 
    print('核心对象：',coreObject)
    #print(objectPoint)
    #遍历所有的核心对象
    while len(coreObject) > 0:
        #resultList.append('--')
        #print(coreObject)
        #随机选择一个核心对象
        coreRandom = random.randrange(0,len(coreObject))
        index = coreObject[coreRandom]
        print('选择的核心对象是：',index)
        order = []
        #计算出这个核心对象的核心距离
        coreDistance = computeCoreDistance(index,objectPoint,minPts,dataSet)
        #print(index,coreDistance)
        print('核心距离：',coreDistance)
        #放在顺序队列中,每一个元素放的是点和可达距离
        order.append(index)
        order.append(coreDistance)
        orderList.append(order)
        #对顺序队列进行循环处理
        while len(orderList) > 0:
            #print(orderList)
            #print('orderList:',orderList)
            firstElement = orderList[0]
            #放入结果队列中去
            resultList.append(firstElement)
            del orderList[0]
            firstElement = firstElement[0]
            #print('firstElement:',firstElement)
            #print('len(objectPoint[firstElement]):',len(objectPoint[firstElement]))
            #print('orderList:',orderList)
            #print('resultList,',resultList)
            #print('objectPoint,',objectPoint[firstElement])
            #print('firstElement',firstElement)
            #拓展这个元素
            if len(objectPoint[firstElement]) > minPts \
                  and (firstElement in coreObject):
                #print('开始')
                coreDistance1 = computeCoreDistance(firstElement,objectPoint,minPts,dataSet)
                #print(firstElement,coreDistance1)
                #删除核心对象中相应的元素列表
                #delete(coreObject,firstElement)
                coreObject.remove(firstElement)
                #objectIndex = searchIndex(firstElement,coreObject)
                for i in objectPoint[firstElement]:
                    #样本点既不在结果队列也不再顺序队列中
                    order = []
                    listIndex = []
                    if not isExistList(i,resultList,listIndex) \
                       and not isExistList(i,orderList,listIndex):
                        #计算每个元素的可达距离
                        reachableDistance = computeReachableDistance(\
                            i,firstElement,dataSet,coreDistance1)
                        order.append(i)
                        order.append(reachableDistance)
                        orderList.append(order)
                        #对顺序队列进行排序
                        orderList = sortOrder(orderList)
                    #样本点在顺序队列中不在结果队列中 
                    elif not isExistList(i,resultList,listIndex) \
                         and isExistList(i,orderList,listIndex):
                        index = listIndex[0]
                        #比较新旧距离
                        reachableDistance = computeReachableDistance(\
                            i,firstElement,dataSet,coreDistance1)
                        #print(orderList[index])
                        #print(i)
                        #如果旧的小于新的，那么代替旧的    
                        if orderList[index][1] > reachableDistance:
                            order.append(i)
                            order.append(reachableDistance)
                            #print(index)
                            #print(orderList)
                            #print(order)
                            orderList[index] =  order
                            #对顺序队列进行排序
                            orderList = sortOrder(orderList)
                
                #print(coreObject)
            #不可拓展的点直接放入orderList中
            elif len(objectPoint[firstElement]) <= minPts and \
                 not isExistList(i,resultList,listIndex) and \
                 not isExistList(i,orderList,listIndex):
                order = []
                reachableDistance = computeReachableDistance(\
                            i,firstElement,dataSet,coreDistance)
                #print('可达距离:',reachableDistance)
                order.append(i)
                order.append(reachableDistance)
                orderList.append(order)
                orderList = sortOrder(orderList)
    return resultList

#生成簇
def generateCluster(resultList,radius,minPits):
    cluster = []
    one_cluster = []
    for i in range(len(resultList) - 1):
        if resultList[i][1] < radius and resultList[i][1] <= resultList[i+1][1]:
            one = resultList[i][0]
            one_cluster.append(one)
        else:
            if len(one_cluster) >= minPits:
                cluster.append(one_cluster)
            one_cluster = []
    if len(one_cluster) > minPits:
        cluster.append(one_cluster)
    for i in range(len(cluster)):
        print('第%d个簇:%s'%(i+1,cluster[i]))
    return cluster                    

if __name__ == '__main__':
    dataSet,labels = createData()
    radius = 0.11
    minPits = 5
    resultList = opticsProcess(dataSet,radius,minPits)
    print('结果列表,',resultList)
    generateCluster(resultList,0.10323,2)
            
        
        
        
    
    
    
 
