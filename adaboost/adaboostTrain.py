import numpy as np
import math
#adaboost算法：
#1.实现弱学习器
#2.实现整个的adaboost算法
#在弱学习器中，使用的是横向和竖向切分，直接选出一个阈值，然后找出错误率最小的
#将之作为我们第一个弱学习器，整个算法会设置循环次数，这里就会有多少个分类器
#在adaboost的整个流程中，计算出整个分类器的权重，并且更新每个样本的权重值
#最后的结果就是先是每个学习器的权重和学习器的分类结果相乘，然后全部加起来
#使用sign函数，分出最后的类别
#adaboost
#1.设置每个样本的初始权重值
#2.放入循环中
#3.将数据、类别和样本权重放入弱学习器中，选出分类效果最好的
#  （1）根据列来循环，计算出步长，用于后面选择阈值 
#  （2）循环阈值来进行切分，找出最好的那个，并且记录列，阈值，正反
#  （3）找出所有列中最好的那个阈值返回
#   补充:这里是只是根据一个维度进行切分，因而每次都是在所有列中选择
#4.根据错误率计算alphas，更新权重值
#5.将此分类放入弱学习器结果中
#6.利用alphas和结果计算值，利用sign来查看错误，错误为0，则完成，否则继续



#用来测试
##def loadData():
##    dataMat = np.mat([[1,2.1],
##                      [2,1.1],
##                      [1.3,1],
##                      [1,1],
##                      [2,1]])
##    classLabel = [1.0,1.0,-1.0,-1.0,1.0]
##    return dataMat,classLabel





#查看每个弱学习器得出的类别结果
#threshold就是切分的阈值
#inEq就是大于还是小于
def weakResult(dataMat,col,threshold,t):
    m = dataMat.shape[0]
    retArray = np.mat(np.ones((m,1)))
    if t == 'lt':
        retArray[dataMat[:,col] <= threshold] = -1
    else:
        retArray[dataMat[:,col] > threshold] = -1
    return retArray
        




#弱分类器
def choiceBestWeak(dataMat,resultMat,Weights):
    m,n = dataMat.shape
    #设置步数
    stpeNum = 10
    #最小错误率
    minError = float('inf')
    result = {}
    classResult = np.mat(np.ones((m,1)))
    #对每个维都进行选择比较
    for i in range(n):
        #计算步长
        maxCol = max(dataMat[:,i])
        minCol = min(dataMat[:,i])
        stpeSize = (maxCol - minCol)/stpeNum
        for j in range(-1,stpeNum+1):
            #计算出阈值
            threshold = float(minCol + float(j)*stpeSize)
            for t in ['lt','gt']:
                classRes = weakResult(dataMat,i,threshold,t)
                #计算出错误率
                error = np.mat(np.ones((m,1)))
                error[classRes == resultMat] = 0
                #print(error)
                #print(Weights)
                errorRate = sum(error.T*Weights)
                #print(errorRate,minError)
                if errorRate < minError:
                    minError = errorRate
                    result['col'] = i
                    result['threshold'] = threshold
                    result['t'] = t
                    classResult = classRes
    return result,minError,classResult

#numIt就是循环次数，返回整个分类器
def adaboostTraining(dataSet,labelSet,numIt = 40):
    dataMat = np.mat(dataSet)
    ResultMat = np.mat(labelSet).T
    weakResult = []
    m,n = dataMat.shape
    #判断数据是否已经分类好了
    result = np.mat(np.zeros((m,1)))
    #设置出初始样本权重值
    Weights = np.mat(np.ones((m,1))/m)
    for i in range(numIt):
        #选择最好的弱学习器
        stumpClass,errorRate,classResult = choiceBestWeak(dataMat,\
                                                          ResultMat,Weights)
        #计算出alphas的值,防止错误率为0时
        alphas = float(0.5*np.log((1-errorRate)/max(errorRate,1e-16)))
        stumpClass['alphas'] = alphas
        #放入到结果学习器中
        weakResult.append(stumpClass)
        #更新样本权重值
        temp = np.multiply(-1*alphas*ResultMat,classResult)
        #print('temp',temp)
        tempTop = np.multiply(Weights,np.exp(temp))
        Weights = tempTop/sum(Weights)
        #查看是否分类完全正确,全部分类正确就完成
        #print('alphas',alphas)
        #print('classResult',classResult)
        result += alphas*classResult
        error = np.multiply(np.sign(result) != ResultMat\
                            ,np.ones((m,1)))
        errorR = error.sum()/m
        #print('errorR',errorR)
        if errorR == 0:
            break
    return weakResult

if __name__ == '__main__':
    dataSet,classLabel = loadData()
    weakResult = adaboostTraining(dataSet,classLabel)
    print(weakResult)
    
    
    
    
