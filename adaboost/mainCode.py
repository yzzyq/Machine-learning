import dataSetExract as dataSE
import adaboostTrain as AT
import numpy as np

dataSet,exeData,classSet = dataSE.extractData()
#训练数据
weakResult = AT.adaboostTraining(dataSet,classSet)
print(weakResult)
#开始进行测试
exeDataMat = np.mat(exeData[:-1])
m,n = exeDataMat.shape
results = np.mat(np.zeros((m,1)))
for i in range(len(weakResult)):
    temp = AT.weakResult(exeDataMat,weakResult[i]['col'],\
                         weakResult[i]['threshold'],weakResult[i]['t'])
    results += weakResult[i]['alphas']*temp
classResult = np.sign(results)
print(classResult)
#查看数据的正确率
correct = 0
for i in range(m):
    if exeData[i][-1] == classResult[i]:
        correct += 1
correct = correct/m*100
print(str(correct)+'%')

    
    
