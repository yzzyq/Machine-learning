import dataSetExract as dataSE
import Diana as diana
import numpy as np

dataSet,labelSet = dataSE.extractData()
trainSet = []
for data in dataSet:
    trainSet.append(data[:-1])
cluster = diana.DianaProcess(trainSet,2)
print('=========')
for i in range(len(cluster)):
    print('第%d个簇：%d' % (i,len(cluster[i])))
