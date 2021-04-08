import random
import numpy as np
import csv
import copy
import math
#神经网络
#1.前向传播：主要是计算出预测值，通过随机初始化权重和偏置，并利用激活函数最终
#            得出预测值
#2.反向传播：前向传播得到预测值之后，我们需要对这个预测值进行评估，也就是损失
#            函数，需要将损失函数降到最小，利用梯度下降（链式法则），来调整
#            权重值和偏置
#迭代这俩个过程，知道满足停止准则
#1.先进行初始化这个神经网络的神经元，并且随机初始化各参数，权重值和偏置
#2.我们要对这个训练集训练好几次，迭代次数
#3.打乱我们的训练集，分为几个小的训练集
#4.利用这些小的训练集依次进行训练，更新权重值和偏置
#5.先进行前向传播，得出结果，保存每个神经元得出的俩个阶段性值（是否激活函数）
#6.利用得出的结果再进行反向传播
#7.利用的是梯度下降来更新权重值
#            1.求出权重E，乘以a就是梯度
#            2.求出第一个后，可以通过第一个得出后面的每个E
#            3.这些都是我们要用来更新
#8.每个样本得出的梯度都要进行相加，得出这个小训练集整个的权重更新值和偏置
#9.利用学习率进行更新
#10.测试集输入进行测试，测试直接在一个前向传播函数中就行
#11.对比，查看数据的准确性

#加载数据
def loadData(fileName):
    dataSet = []
    with open(fileName) as file:
       File = csv.reader(file,delimiter=',')
       dataSet = list(File)
       for i in range(len(dataSet)):
           #将字符串转化为浮点数,数据量有点大
           dataSet[i] = [float(x) for x in dataSet[i]] 
    return dataSet

#将数据集分为训练集和测试集
def splitDataSet(dataSet,splitRatio):
    trainSetSize = int(len(dataSet)*splitRatio)
    trainSet = []
    #测试集
    exeSet = dataSet
    while len(trainSet) < trainSetSize:
        index = random.randrange(len(exeSet))
        data = copy.deepcopy(dataSet[index])
        trainSet.append(data)
        del exeSet[index]     
    return trainSet,exeSet

class Network:
    def __init__(self,net):
        #神经网络层数的个数
        self.net = net;
        #神经网络有几层
        self.netNum = len(net)
        #初始化权重值
        self.weights = [np.random.randn(x,y) for x,y in zip(net[1:],net[:-1])]
        #初始化偏执
        self.bs = [np.random.randn(x,1) for x in net[1:]]

    #前向传播
    def forwardSpread(self,data):
        for w,b in zip(self.weights,self.bs):
            #print(np.dot(w,data) + b)
            data = self.sigmoid(np.dot(w,data) + b)
            #print(np.dot(w,data) + b)
        print('data:',data)
        return data
            
    #激活函数使用sigmoid
    def sigmoid(self,x):
        #print(x)
        return 1/(1 + np.exp(-x))

    #对激活函数的求导
    def sigmoid_derivation(self,x):
        return np.multiply(self.sigmoid(x),1-self.sigmoid(x))

    def generateResult(self,resultMat):
        result = np.zeros((2,1))
        result[int(resultMat),0] = 1  
        return result

    #开始对整个数据进行训练
    #minPts每次迭代的时候，总数据集划分成小的数据集
    #num就是迭代次数
    def neuralNetworkProcess(self,dataSet,minPits_sizes,num,learnRate):
        #m,n = dataMat.shape
        #对所有的数据进行迭代
        #print('开始进行迭代。。')
        for i in range(num):
            #打乱所有的数据
            random.shuffle(dataSet)
            #将打乱的所有数据划分成小的数据进行测试
            minPts = [dataSet[i:i+minPits_sizes] \
                       for i in range(0,len(dataSet),minPits_sizes)]
            #对其中的每个数据集进行训练
            for minPt in minPts:
                minPtMat = np.mat(minPt)
                #根据每个小样本进行更新w,b
                self.updateWeightAndB(minPtMat,learnRate)

    #根据小样本集更新权重和偏置
    def updateWeightAndB(self,minPtMat,learnRate):
        m,n = minPtMat.shape
        #进行迭代相加每次更新
        nebla_w = [np.zeros(weight.shape) for weight in self.weights]
        nebla_b = [np.zeros(b.shape) for b in self.bs]
        #对每条数据进行计算更新
        for i in range(m):
            #取出每个数据的数据和结果
            data = minPtMat[i,:-1]
            result = self.generateResult(minPtMat[i,-1])
            
            #更新权重值的函数
            new_nebla_w,new_nebla_b = self.backPro(data,result)
            #print(nebla_w)
            #print(new_nebla_w)
            nebla_w = [new_w+w for new_w,w in zip(new_nebla_w,nebla_w)]
            nebla_b = [new_b+b for new_b,b in zip(new_nebla_b,nebla_b)]
        #采用学习率对小样本集更新进行更新
        self.weights = [w - (learnRate/m)*new_w \
                        for w,new_w in zip(self.weights,nebla_w)]
        self.bs = [b - (learnRate/m)*new_b \
                   for b,new_b in zip(self.bs,nebla_b)]

    #根据每个样本更新权重和偏置
    def backPro(self,data,result):
        #测试数据的类别
        runResult = data.transpose()
        #距离我们更新的权值和偏执
        nebla_w = [np.zeros(weight.shape) for weight in self.weights]
        nebla_b = [np.zeros(b.shape) for b in self.bs]
        #print(data,result)
        #记录我们每次计算的结果
        #print('前向传播开始，激活函数使用sigmoid函数。。')
        z_results = []
        a_sigmoid_results = [runResult]
        #先对数据进行前向传播
        for w,b in zip(self.weights,self.bs):
            z = np.dot(w,runResult) + b
            #print(w.shape,runResult.shape)
            #print('权重计算:',np.dot(w,runResult))
            z_results.append(z)
            runResult = self.sigmoid(z)
            a_sigmoid_results.append(runResult)
        #print('权重相乘，外加偏置：',z_results)
        #print('激活函数后：',a_sigmoid_results)
        #开始进行后向传播
        #先计算后向的第一个，然后根据推导出的公式依次计算权重和偏置
        #print('误差：',a_sigmoid_results[-1])
        #print('-result.T',result.T)
        #print('开始后向传播')
        delta = np.multiply(a_sigmoid_results[-1]-result,\
                            self.sigmoid_derivation(z_results[-1]))          
        nebla_b[-1] = delta
        #print('delta:',delta)
        #print(a_sigmoid_results)
        #print('结果集:',a_sigmoid_results[-1])
        nebla_w[-1] = np.dot(delta,a_sigmoid_results[-2].T)
        for i in range(2,self.netNum):
            #print(i)
            z = z_results[-i]
            #对激活函数的求导
            sp = self.sigmoid_derivation(z_results[-i])
            #利用后面的求出前面的
            delta = np.multiply(np.dot(self.weights[-i+1].T,delta),sp)
            nebla_b[-i] = delta
            nebla_w[-i] = np.dot(delta,a_sigmoid_results[-i-1].T)
        return nebla_w,nebla_b

    #对测试集进行预测 
    def evaluate(self,test_data):
        data_one = np.mat(test_data[:-1]).T
        #print(self.forwardSpread(data_one))
        #获得预测结果
        test_results = np.argmax(self.forwardSpread(data_one))
        print('test_results:',test_results)
        return test_results
         
         
if __name__ == '__main__':
    #加载数据
    dataSet = loadData('text.csv')
    #dataSet = loadData('pima-indians-diabetes.csv')
    #70%是训练集，30%是测试集
    trainSet,exeSet = splitDataSet(dataSet,0.7)
    nets = Network([len(trainSet[0])-1,3,2])
    #print(nets.bs)
    nets.neuralNetworkProcess(trainSet,10,300,0.3)
    print('训练后的权重值：')
    print(nets.weights)
    print('训练后的偏置：')
    print(nets.bs)
    correct = 0
    for data in exeSet:
        #print('数据',data)
        result = nets.evaluate(data)
        print('测试的结果:%d    实际结果：%d'%(result,data[-1]))
        if result == data[-1]:
            correct += 1
    print('预测的精度：%d'% correct/len(exeSet))
        
    
            
                   
                
        
        
