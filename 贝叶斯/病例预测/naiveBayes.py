#贝叶斯算法
import csv
import random
import math
import copy

#整个流程：
##1.处理数据：从CSV文件载入数据，分为训练集和测试集
##      1.将文件中字符串类型加载进来转化为我们使用的数字
##      2.数据集随机分为包含67%的训练集和33%的测试集
##
##2.提取数据特征：提取训练数据集的属性特征，以便我们计算概率并作出预测
##      1.按照类别划分数据
##      2.写出均值函数
##      3.写出标准差函数
##      4.计算每个类中每个属性的均值和标准差（因为这里是连续型变量，也可以使用区间）
##      5.写个函数将上面过程写入其中
##
##3.预测
##      1.根据上述计算出的均值和方差，写出函数是计算高斯概率密度函数
##      2.计算值对每个类别的高斯概率分布
##
##3.单一预测：使用数据集的特征生成单个预测
##      1.比较那个类别的概率更大，就输出哪个
##      
##4.评估精度：评估对于测试数据集的预测精度作为预测正确率
##      1.多重预测：基于给定测试数据集和一个已提取特征的训练数据集生成预测，就是生成了很多预测.
##      2.计算精度，看正确率



#加载数据
# 1. Number of times pregnant
# 2. Plasma glucose concentration a 2 hours in an oral glucose tolerance test
# 3. Diastolic blood pressure (mm Hg)
# 4. Triceps skin fold thickness (mm)
# 5. 2-Hour serum insulin (mu U/ml)
# 6. Body mass index (weight in kg/(height in m)^2)
# 7. Diabetes pedigree function
# 8. Age (years)
# 9. Class variable (0 or 1)

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

#按照类别划分数据，这里就是0和1
def splitDataSetByClass(dataSet):
    dataClass = {}
    for data in dataSet:
        key = data[-1]
        if key not in dataClass.keys():
            dataClass[key] = []
        del data[-1]    
        dataClass[key].append(data)
    return dataClass

#因为数据中的数值都是连续型的
#计算均值
def averageData(dataSet):    
    return sum(dataSet)/len(dataSet)
    
#计算方差
def varianceData(dataSet):
    aver = averageData(dataSet)
    temp = 0.0
    dataSetTemp = dataSet
    for data in dataSet:
        temp += math.pow(data - aver,2)+1
    return math.sqrt(temp/(len(dataSet)+2))

#计算每个属性的均值和方差
def attributesNormal(dataSet):
    dataClass = splitDataSetByClass(dataSet)
    dataNormal = {}
    
    #每个类别进行循环
    for dataAttri in dataClass.keys():
        data = dataClass[dataAttri]
        dataNormal[dataAttri] = []
        
        
        #每列元素组合在一起
        dataAttribute = zip(*data)
        
        #计算每列的均值和方差
        for dataCol in dataAttribute:      
            attri = []  
            aver = averageData(dataCol)
            variance = varianceData(dataCol)   
            attri.append(aver)
            attri.append(variance)
            dataNormal[dataAttri].append(attri)
    print('dataNormal:',dataNormal)
    return dataNormal

#计算每个属性高斯密度函数
def normalFunction(value,data):
    aver = value[0]
    variance = value[1]  
    temp = math.exp(-(float)(math.pow(data-aver,2))/(2*math.pow(variance,2)))  
    return (1/math.sqrt(2*(math.pi)*variance))*temp


#计算每个类别的每个属性密度函数值
def Normal(dataNormal,exeData):
    bestLabel = None
    bestScoer = 0.0
    #比较俩个类别，谁大就是谁
    for key in dataNormal.keys():  
        values = dataNormal[key]     
        normalClass = 1
        for i in range(len(values)):
            normalClass *= normalFunction(values[i],exeData[i])
          
        if normalClass > bestScoer:
            bestScoer = normalClass
            bestLabel = key
    return bestLabel

#模型的准确率
def accuracy(results,exeSet):
    correctDecision = []
    for data in exeSet:
        print(data)
        correctDecision.append(data[-1])
    sumExeDataSet = len(exeSet)
    correctNum = 0
    #print(len(correctDecision))
    #print(len(results))
    for i in range(sumExeDataSet):
        if correctDecision[i] == results[i]:
            correctNum += 1
    return correctNum/sumExeDataSet


#加载数据
dataSet = loadData('pima-indians-diabetes.csv')
#70%是训练集，30%是测试集
trainSet,exeSet = splitDataSet(dataSet,0.7)
#得出所有的属性的均值和方差
dataNormal = attributesNormal(trainSet)

#对每个数据计算结果
results = []
for exe in exeSet: 
    result = Normal(dataNormal,exe)
    results.append(result)

#测试准确度
num = accuracy(results,exeSet)
print(num)



    


