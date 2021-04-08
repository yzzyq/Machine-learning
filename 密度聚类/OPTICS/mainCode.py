import dataSetExract as dataSE
import Optics

dataSet,labelSet = dataSE.extractData()
radius = 600
minPts = 20
trainSet = []
for data in dataSet:
    trainSet.append(data[:-1])
resultList = Optics.opticsProcess(trainSet,radius,minPts)
print('生成的结果列表：')
print(resultList)
print('从结果列表中根据E和minpts查找簇,这里的E为557，minpts为10：')
Optics.generateCluster(resultList,557,10)

