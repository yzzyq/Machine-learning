import math
from scipy.stats import multivariate_normal
import numpy as np
import matplotlib.pyplot as plt
#EM算法
#输入：数据集和高斯混合成分个数K
#1.先初始化高斯混合分布的模型参数
#2.开始进行迭代，先进行E步，就是计算每个数据在各混合成分生成的概率
#3.进行M步，极大似然估计，利用这些概率计算各高斯的均值、协方差、混合系数
#4.将模型系数更新
#5.满足条件的时候退出停止
#6.然后遍历所有的数据，算出每个数据相应的簇

#高斯混合模型建立的全过程
#K表示模型个数
#times表示迭代次数
def GMM_process(dataSet,K,times):
    dataSetMat = np.mat(dataSet)
    #print(dataSetMat)
    #先进行初始化
    model_weights,model_exception,model_covariance = init_param(dataSetMat,K)
    print('model_weights,',model_weights)
    print('model_exception,',model_exception)
    print('model_covariance,',model_covariance)
    #迭代进行算法
    for i in range(times):
        #print('print(model_covariance):',model_covariance)
        #先进行E步
        allDataToModel = getException(\
            dataSetMat,model_weights,model_exception,model_covariance)
        #再进行M步
        model_weights,model_exception,model_covariance = \
                                        maximize(dataSetMat,allDataToModel)
    #求除了这个GMM，之后，开始利用它来聚类
    alldata = getException(\
            dataSetMat,model_weights,model_exception,model_covariance)
    #print(alldata)
    #取出每个数据中的最大的划分到相应的簇中
    datasClass = alldata.argmax(axis=1).flatten().tolist()[0]
    clusterAll = [[] for i in range(K)]
    #print(datasClass)
    for i in range(len(datasClass)):
        dataClass = datasClass[i]
        clusterAll[dataClass].append(dataSet[i])
    return clusterAll


#多元高斯模型数值的计算
def one_gussian(data,k_exception,k_covariance):
    temp = multivariate_normal(mean=k_exception,cov=k_covariance)
    return temp.pdf(data)

#初始化数据
def init_param(dataSetMat,K):
    dataNum,featureNum = dataSetMat.shape
    #初始化每个模型的权重
    weights = np.array([1/K]*K)
    #初始化每个模型的数学期望
    exceptions = np.random.rand(K,featureNum)
    #初始化多元高斯模型的协方差矩阵
    #因为每个特征都是独立的，所以这里的协方差是对角矩阵
    cov = np.array([np.eye(featureNum)]*K)
    return weights,exceptions,cov

#E步
def getException(dataSetMat,model_weights,model_exception,model_covariance):
    dataNum,featureNum = dataSetMat.shape
    K = model_weights.shape[0]
    #初始化数据在各混合成分生成的概率矩阵
    resultMat = np.mat(np.zeros((dataNum,K)))

    #计算各模型中所有样本出现的概率
    temp = np.zeros((dataNum,K))
    #print(dataSetMat)
    for i in range(K):
        temp[:,i] = one_gussian(dataSetMat,model_exception[i],\
                                model_covariance[i])
    #print('temp',temp)
    #计算每个模型对每个样本的响应度
    for i in range(K):
##        print('temp',temp)
##        print(model_weights[i])
##        print(temp[:,i])
        tempK = model_weights[i]*temp[:,i]
        tempArray = [[i] for i in tempK]
        tempArray = np.mat(tempArray)
        resultMat[:,i] = tempArray
    #print('resultMat,',resultMat)
    for i in range(dataNum):
        resultMat[i,:] /= np.sum(temp[i,:])
    print('resultMat',resultMat)
    return resultMat

#M步
def maximize(dataSetMat,resultMat):
    #print(resultMat)
    dataNum,featureNum = dataSetMat.shape
    #模型数
    K = resultMat.shape[1]
    #初始化
    model_weights = np.zeros(K)
    model_exception = np.zeros((K,featureNum))
    #model_covariance = np.array([np.eye(featureNum)]*K)
    model_covariance = []
    #更新每个模型的参数
    for i in range(K):
        #第K个模型对所有样本的响应度之和
        sumAll = np.sum(resultMat[:,i])
        #开始更新期望值
        model_exception[i,:] = np.sum(np.multiply(dataSetMat,resultMat[:,i]),\
                                      axis=0) / sumAll
        #更新协方差
        covariance = (dataSetMat - model_exception[i]).T * \
                     np.multiply((dataSetMat - model_exception[i]),\
                                 resultMat[:,i])/sumAll
        #print(covariance)
##        covarianceArr = [covariance for i in range(featureNum)]
##        print(covarianceArr)
        model_covariance.append(covariance)
        #model_covariance[i] = np.mat(np.diag(covarianceArr))
        model_weights[i] = sumAll / dataNum
    model_covariance = np.array(model_covariance)
    #print('model_covariance',model_covariance)
    return model_weights,model_exception,model_covariance

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
    plt.title('EM')
    plt.xlim(-10,10)
    plt.xticks(())
    plt.ylim(-10,10)
    plt.yticks(())
    plt.show()
 

    
if __name__ == '__main__':
    dataSet,labels = createData()
    dataSetMat = np.mat(dataSet)
    clusterAll = GMM_process(dataSet,3,50)
    print(clusterAll)
    Visualization(clusterAll)
    
     
    
    
    
    


    
