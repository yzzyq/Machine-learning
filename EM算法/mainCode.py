#总体的代码
import dataSetExract as dataSE
import EMAlgorithm as EM
import numpy as np

dataSet = dataSE.extractData()
dataSet = np.array(dataSet)
print(dataSet)
aa=aa
clusterAll = EM.GMM_process(dataSet,3,50)
print(clusterAll)
EM.Visualization(clusterAll)



