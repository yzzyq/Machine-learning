import random
import math
import copy
import Tree
import dataSetExract as dataSE
from collections import Counter
#随机森林
#随机森林中有很多树组成，但是这些树都是没有关联的（限制用于构建树木的特征）
#这里分为行采样和列采样
#1.数据的随机性选择
#2.待选特征的随机选择，1.每一个结点都是随机选择一些特征，选择其中最好的特征
#                     ，通常是log2d
#                      2.也可以每棵树只选择固定的特征子集来选择
#这里我们实现的随机树，
#1.有放回的进行数据采样，大小为数据集大小，因而每个数据集包含重复的元素，
#2.每个决策树都在我们随机选择的数据集中进行建立
#3.在决策树建立的时候，每个节点的选择，我们都是随机选择log2d个特征进行比较
#选出最好的那个特征
#4.最终，测试时候采用投票法，票数最高的那个就是我们得出的

#又放回的随机选取数据和特征
def randomSample(dataSet,labelSet):
    lenData = len(dataSet)
    logLenFeature = math.log(len(labelSet))
    labelCopy = copy.deepcopy(labelSet)
    #子树的数据集
    childData = []
    #选取的特征
    childFeatures = []
    #未使用的数据
    noUseData = [0 for i in range(lenData)]
    #选取特征
    while len(childFeatures) < logLenFeature:
        #print('labelSet长度：',len(labelSet))
        randomNum = random.randint(0,len(labelCopy)-1)
        childFeatures.append(labelCopy[randomNum])
        del labelCopy[randomNum]
    #print(childFeatures)
    #有放回的选取数据
    while len(childData) < lenData:
        randomNum = random.randint(0,lenData-2)
        #print('randomNUM',randomNum)
        data = []
        for num in childFeatures:
            #print(num)
            #print('dataSet',len(dataSet[randomNum]))
            #print(dataSet[randomNum][num])
            data.append(dataSet[randomNum][num])
        data.append(dataSet[randomNum][-1])
        childData.append(data)
        #print('======================')
        #print(data)
        noUseData[randomNum] += 1
    
    return childData,childFeatures,noUseData

#使用过最少的30%的数据作为测试数据
def produceData(choiceDataNum,dataSet):
    testDataNum = 0.3*len(choiceDataNum)
    testData = []
    dataCopy = copy.deepcopy(choiceDataNum)
    while len(testData) < testDataNum:
        minData = dataCopy.index(min(dataCopy))
        testData.append(dataSet[minData])
        del dataCopy[minData]
    return testData
        
if __name__ == '__main__':
    dataSet,labelSet = dataSE.extractData()
    #森林中数的个数
    numTree = 50
    #森林
    forest = []
    #查看每个数据的选中情况
    choiceDataNum = [ 0 for i in range(len(dataSet))]
    #建立每棵决策树
    for i in range(numTree):
        #首先选出数据集
        #print(labelSet)
        childData,chidFeatures,noUseData = randomSample(dataSet,labelSet)
        #建立决策树
        childTree = Tree.buildTree(childData,chidFeatures)
        Tree.printTree(childTree)
        forest.append(childTree)
        for i in range(len(noUseData)):
            choiceDataNum[i] += noUseData[i]
    testData = produceData(choiceDataNum,dataSet)
    results = []
    correct = 0
    #开始测试每个测试集
    for data in testData:
        results = []
        for tree in forest:
            result = Tree.classify(data,tree,labelSet)
            #print(list(result.keys()))
            results.append(list(result.keys()))
        #print(results)
        feaNum = 0
        noFeaNum = 0
        resultData = 'feafits'
        #采用投票法，票数最多的就是类别
        for i in range(len(results)):
            #print('result[i]',results[i])
            if results[i][0] == 'feafits':
                feaNum += 1
            else:
                noFeaNum += 1
        #print(feaNum,noFeaNum)
        if feaNum < noFeaNum:
            resultData = 'nofeafits'
        print('结果是',resultData)
        results.append(resultData)
        print('实际结果是：',data[-1])
        if resultData == data[-1]:
            correct += 1
    ccur = (correct / len(testData))*100
    print('精确度:',ccur)
    
    
    



