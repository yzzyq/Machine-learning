import neuralNetwork
import dataSetExract as dataSE

dataSet = dataSE.extractData()
trainSet,exeSet = neuralNetwork.splitDataSet(dataSet,0.7)
nets = neuralNetwork.Network([len(trainSet[0])-1,8,9,2])
#print(nets.bs)
print('编写的神经网络有俩层隐藏层，第一层有10层，第二层有300，学习率是0.3')
nets.neuralNetworkProcess(trainSet,10,300,0.3)
print('训练后的权重值：')
print(nets.weights)
print('训练后的偏置：')
print(nets.bs)
correct = 0
for data in exeSet:
    result = nets.evaluate(data)
    print('测试的结果:%d    实际结果：%d'%(result,data[-1]))
    if result == data[-1]:
        correct += 1
print(correct/len(exeSet))



