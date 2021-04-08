import random
import csv
#提取数据集
def loadDataSet(filename):
    dataSet = []
    labelSet = []
    with open(filename) as file:
        File = csv.reader(file,delimiter=',')
        data = list(File)
        for i in range(len(data)):
            dataSet.append([float(data[i][0]),float(data[i][1])/50])
            if float(data[i][-1]) == 0:
                data[i][-1] = -1
            labelSet.append(float(data[i][-1]))
    return dataSet,labelSet
 
#选取第二个要优化的系数
def selectRandom(i,m):
    j = i
    while i == j:
        j = int(random.uniform(0,m))
    return j

#将之限制在范围内
def restrictRange(num,top,bottom):
    if num > top:
        num = top
    elif num < bottom:
        num = bottom
    return num


