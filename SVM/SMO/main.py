import SMOTrain as train
import generalTool as tool


dataSet,labelSet = tool.loadDataSet('text.csv')
print(labelSet)
b,alphas = train.smoSimple(dataSet,labelSet,0.9,10,0.01)
print("b：",b)
print('alphas:',alphas)
