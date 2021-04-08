import dataSetExract as dataSE
import Birch
from sklearn.manifold import TSNE


dataSet = dataSE.extractData()
node = Birch.CrateCFTree(dataSet,3,3,33)
cluster = Birch.printTree(node)
#Birch.Visualization(node)
Birch.Visualization(cluster)


