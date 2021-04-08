import dataSetExract as dataSE
import Dbscan as DB

dataSet,labelSet = dataSE.extractData()
radius = 1000
minPts = 20
trainSet = []
for data in dataSet:
    trainSet.append(data[:-1])
cluster,k = DB.DbscanProcess(trainSet,radius,minPts)
print('分成的簇为,',cluster)
