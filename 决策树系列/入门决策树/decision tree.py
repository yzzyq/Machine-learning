import math
import BorrowingInformation as bi

#求出一个属性值的每个决策的数目
def entropyDecision(rows):
    decisionChoice = {}
    for row in rows:
        decision = row[-1]
        if decision not in decisionChoice:
            decisionChoice[decision] = 0
        decisionChoice[decision] += 1
    return decisionChoice


#求一个属性值的信息熵
def entropy(rows):
    gainFactor = 0
    length = len(rows);
    #求出一个属性值的每个决策的数目
    decisionChoice = entropyDecision(rows)
    #对这个属性值求出熵值    
    for value in decisionChoice.keys():
        ratio = float(decisionChoice[value])/length
        gainFactor -= ratio*(math.log(ratio)/math.log(2))
    return gainFactor

#提取出所有满足一个特征的数据集
def splitValue(dataSet,col,value):
    relData = []
    for data in dataSet:
        if data[col] == value:
            #已经用过的属性列，就抛去
            colRows = list(data[:col])
            colRows.extend(data[col+1:])
            relData.append(colRows)
    return relData


#选择出最好的属性
def chioceBest(dataSet,entro = entropy):
    #计算出整个的熵值
    score_all = entropy(dataSet)
    print('整体信息熵', score_all)
    #最好的特征
    bestAttri = -1  
    #最好特征的增益因子
    bestAttriGain = 0.0
    #属性的个数
    attributes = len(dataSet[0]) - 1
    #计算每个属性的条件熵，并选出最好的那个
    for col in range(attributes):
        #得到这个列的所有的值
        data_col = [example[col] for example in dataSet]
        #得出这一属性的值
        values_col = set(data_col)
        col_entropy = 0.0
        #属性值的条件熵
        for value in values_col:
            #得出相关属性值的所有行数
            value_dataSet = splitValue(dataSet,col,value)
            newEntropy = entropy(value_dataSet)
            print('信息熵', newEntropy)
            ratio = len(value_dataSet)/len(dataSet) 
            col_entropy += ratio*newEntropy
        #得到增益因子   
        attributeGain = score_all - col_entropy
        print('信息增益:', attributeGain)
        if attributeGain > bestAttriGain:
            bestAttriGain = attributeGain
            bestAttri = col
    return bestAttri


#递归建树
def buildTree(dataSet,labelSet):
    decision = [example[-1] for example in dataSet]
    decisionType = set(decision)
    #如果熵值为0
    if len(decisionType) == 1:
        return decisionType
    
    #这里的树采用了字典，二叉树的话，之后再实现
    key = chioceBest(dataSet)
    keyLabel = labelSet[key]
    #构造决策树
    myTree = {keyLabel:{}}
    #使用完了就删除
    del labelSet[key]
    bestCol = [example[key] for example in dataSet]
    valueCol = set(bestCol)
    for value in valueCol:
        subLabel = labelSet[:]
        myTree[keyLabel][value] = buildTree(splitValue(dataSet,key,value),subLabel)
    return myTree


#存储决策树到磁盘中
def storeTree(decisionTree,fileName):
    with open(filename,'wb') as fw:
        pickle.dump(decisionTree,fw)

#从磁盘中取出决策树
def getTree(fileName):
    fr = open(fileName,'rb')
    return pickle.load(fr)

#决策
def classifier(decisionData,decisionTree,labelSet):
    if not isinstance(decisionTree,dict):
        return decisionTree
    feature = list(decisionTree.keys())[0]
    value = decisionData[labelSet.index(feature)]
    sub_decisionTree = decisionTree[feature][value]
    return classifier(decisionData,sub_decisionTree,labelSet)

#后剪枝,先不看，损失函数的计算，需要更改一下数据结构
def postPruningTree(decisionTree,dataSet,minGain,labelSet):
    value = str(list(decisionTree.values()))
    firstKey = list(decisionTree.keys())[0]
    value = decisionTree[firstKey]
   
    for num in value.keys():     
        if not isinstance(value[num],set):
            #不是叶子节点，继续向下递归
            col = labelSet.index(firstKey)
            data = splitValue(dataSet,col,num)
            return postPruningTree(value[num],dataSet,minGain,labelSet)
        
        #就是叶子节点，比较能不能进行合并
        entropyLefSum = 0.0
        for num in value.keys():
            col = labelSet.index(firstKey)
                  
            data = splitValue(dataSet,col,num)
            entropyLefSum -= float(len(data)/len(dataSet))*entropy(dataSet)
        gain = entropy(dataSet) - entropyLefSum
        print(gain)
        print(minGain)
        if gain < minGain:
            decisionChoice = entropyDecision(dataSet)
            maxNum = 0
            maxDecision = list(decisionChoice.keys())[0]
            print(maxDecision)
            for key in decisionChoice.keys():
                print(key)
                if decisionChoice[key] > maxNum:
                    maxDecision = key
                    print(maxDecision)
            decisionTree = maxDecision
    return decisionTree
    

if __name__ == '__main__':
    #进行深拷贝
    label1 = bi.labelSet[:]
    label2 = bi.labelSet[:]
    dataSetTemp = bi.dataSet[:]
    myTree = buildTree(dataSetTemp,label1)
#    print(myTree)
    data = [2,1,0,2]
#    decision = classifier(data,myTree,bi.labelSet)
#    myTree = postPruningTree(myTree,bi.dataSet,0.1,label2)
    print(myTree)
    
