import createFPgrowth as fp
import searchFrequently as sf
import dataSetExract as dse

dataSet = dse.extractData()
dataDict = fp.crateInitData(dataSet)
reTree,headerTable = fp.createTree(dataDict,8)
reTree.disp()
myFreqList = []
sf.mineTree(reTree,headerTable,8,set([]),myFreqList)
print(myFreqList)


