import generalTool
import PlattSMOTrain as pst
import numpy as np



#SVM的主要运行过程
dataSet,labelSet = generalTool.loadDataSet('text.csv')
exeDataSet,exeLabel = generalTool.splitDataSet(dataSet,labelSet,0.8)
b,alphas = pst.SMOTrain(dataSet,labelSet,0.6,0.001,50)
print('b:',b)
print('alphas:',alphas)
w = pst.calcWeights(alphas,labelSet,dataSet)
print('w:',w)
exeDataSet = np.mat(exeDataSet)
m,n = exeDataSet.shape
results = []
for i in range(m):
    result = float(exeDataSet[i,:]*np.mat(w) + b)
    if result <= 0:
        result = -1
    else:
        result = 1
    results.append(result)
correct = 0
print(results)
print(exeLabel)
for i in range(len(results)):
    if results[i] == exeLabel[i]:
        correct += 1
print('精确度：',correct/len(results))


