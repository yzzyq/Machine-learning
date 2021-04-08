#PCA
#将方差作为最大可分性的标准，PCA假设的就是方差越大，信息量越大
#利用特征向量和特征值对矩阵进行了分解
#过程：
#1.对数据减去平均值，这样一行平均值为，之后更好计算
#2.计算协方差
#3.对这个协方差求特征值和特征向量
#4.对特征值进行排序，拿出K个最大的特征值，这里K就是维度
#5.找出相应的特征向量
#6.数据矩阵乘以特征向量，得到所有的降维后的数据

import numpy as np
import csv
import dataSetExract as dataSE
import matplotlib.pyplot as plt

#加载数据
def loadData(fileName):
    dataSet = []
    with open(fileName) as file:
        File = csv.reader(file,delimiter=',')
        dataSet = list(File)
        for i in range(len(dataSet)):
            dataSet[i] = [float(x) for x in dataSet[i]]

    return dataSet

#数据的维度
def PcaProcess(dataSet,k):
    dataSetMat = np.mat(dataSet)
    meanMat = np.mean(dataSetMat)
    print(meanMat)
    #去平均值
    dataSetProcess = dataSetMat - meanMat
    #print(dataSetProcess)
    #计算协方差,这里的rowvar=0就是一行代表一个数据，如果不加就是整个代表一个数据
    #covMat = np.cov(dataSetProcess,rowvar=0)
    covMat = np.cov(dataSetProcess,rowvar=0)
    #计算它的特征值和特征向量
    eigenValues,FeatureVector = np.linalg.eig(covMat)
    #对特征值降序排序
    sortVlaues = np.argsort(-eigenValues)
    #选出前K个特征值
    sortVlaues = sortVlaues[:k]
    #选出相应的特征向量
    baseVector = FeatureVector[:,sortVlaues]
    #数据降维
    print(sortVlaues)
    reductionData = np.dot(dataSetProcess,baseVector)
    return reductionData

def printScatter(dataSet):
    colors = ['b','y','r','k','c','m','g','#e24fff','#524C90','#845868']
    X = np.array(dataSet[:,0].real)
    Y = np.array(dataSet[:,1].real)
    print(X)
    print(Y)
    plt.scatter(X,Y,s=25,c=colors[1])
    plt.xlim(-30,30)
    plt.xticks(())
    plt.ylim(-30,30)
    plt.yticks(())

    plt.show()
    
    


if __name__ == '__main__':
    #dataSet = loadData('text.csv')
    dataSet = dataSE.extractData()
    reductionData = PcaProcess(dataSet,2)
    print('reductionData:',reductionData)
    printScatter(reductionData)
    
