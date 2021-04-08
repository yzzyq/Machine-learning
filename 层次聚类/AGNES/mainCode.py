import dataSetExract as dataSE
import AGNES as AG

dataSet,labelSet = dataSE.extractData()
trainSet = []
for i in range(len(dataSet)):
    trainSet.append(dataSet[i][:-1])
    
cluster = AG.agnesProcess(trainSet,3)
print(cluster)

