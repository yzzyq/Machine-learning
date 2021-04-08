import dataSetExract as extract
import numpy as np
import random
import math
#k-近邻算法:1.计算已知类别的点和当前点的之间距离
#           2.按照距离递增次序排序  
#           3.选取与当前点最小的k个点
#           4.确定前K个点所在类别的出现频率
#           5.返回前k个点出现频率最高的类别作为当前点的预测分类

#将数据集划分为我们所需的训练集和测试集
def splitDataSet(dataSet,ratio):
    num = int(len(dataSet)*ratio)
    trainSet = []
    while len(trainSet) < num:
        randI = random.randrange(len(dataSet))
        trainSet.append(dataSet[randI])
        del dataSet[randI]
    return trainSet,dataSet

#dataSet  已知类别的训练集
#labelSet 类别集
#k        选取的前k个值
#data     数据
def classify(dataSet,labelSet,k,data):
    #使用欧式距离进行计算
    #得到数据的行数
    rows = int(len(dataSet) - 1)
    distance = []
    for i in range(rows):
        sumData = 0
        for j in range(len(data) - 1):
            sumData += math.pow((dataSet[i][j] - data[j]),2)
        distance.append(math.sqrt(sumData))
    #print(distance)
    distance = np.mat(distance)
    #进行排序
    #print(distance)
    sortedDistance = distance.argsort()
    #print(sortedDistance)
    #取出距离最小的k个值
    dataFea = 0
    unDataFes = 0
    #确定前K个点所在类别的出现频率
    for i in range(k):  
        index = int(sortedDistance[0,i])
        if dataSet[index][-1] == 'feafits':
            dataFea += 1
        elif dataSet[index][-1] == 'nofeafits':
            unDataFes += 1
    #返回前k个点出现频率最高的类别作为当前点的预测分类
    if dataFea > unDataFes:
        return 'feafits'
    else:
        return 'nofeafits'
   


#查看数据的精确性
def precise(exeSet,results):
    correct = 0
    for i in range(len(exeSet)):
        if exeSet[i][-1] == results[i]:
            correct += 1
    return correct/len(results)


dataSet,labelSet = extract.extractData()
#将数据集70%化分为训练集，30%划分为测试集
trainSet,exeSet = splitDataSet(dataSet,0.7)
##for data in trainSet:
##    print(data)
results = []
for data in exeSet:
    dataType = classify(trainSet,labelSet,7,data)
    results.append(dataType)
print(results)
preciseData = precise(exeSet,results)
print(preciseData)
