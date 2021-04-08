#apriori就是先寻找频繁项集，然后在频繁项集中寻找关联规则
#       采用的是先验性质,一个频繁项集的所有子集都是频繁的
#               反过来就是不频繁的子集的超集都是不频繁的
#步骤：
#   （1）选择频繁项集
#      1.创建初始的项集，就是单个集
#      2.从单个项集中选出频繁项集（支持度）
#      3.从这些频繁项集中再组合，形成项集
#      4.再进行选择，利用支持度选择频繁项集
#      5.这样一直进行下去，知道都不满足最小支持度，就是选择除了所有的频繁项集
#   （2）从频繁项集中选出关联规则
#      1.单个元素的频繁项集无法产生出关联规则，因此从俩个元素的频繁项集开始
#      2.当只有俩个元素的时候，直接利用置信度选择出关联规则
#      3.当有多个元素的时候，进行组合，然后计算出关联规则，如果只有一条关联
#        规则满足要求，那么无法再组合成关联规则，如果是多个，那么可以再次组合
#        成关联规则进行检查#
import dataSetExract as dataSE

#创建出初始项集
def createInitialSet(dataSet):
    items = []
    for data in dataSet:
        for item in data:
            if [item] not in items:
                items.append([item])
    items.sort()
    return map(frozenset,items)

#查找出频繁项集
def searchFrequent(dataSet,ItemSet,minSupport):
    items = []
    supportData = {}
    lenData = len(dataSet)
    for item in ItemSet:
        num = 0
        for data in dataSet:
            if item.issubset(data):
                num += 1
        #计算支持度
        support = float(num / lenData)
        if support >= minSupport:
            items.append(item)
            supportData[item] = support
    return items,supportData

    
#组合成超集
def createSuperSet(frequentlySet,k):
    lenData = len(frequentlySet)
    superSet = []
    for i in range(lenData):
        for j in range(i+1,lenData):
            temp1 = list(frequentlySet[i])[:k-2]
            temp2 = list(frequentlySet[j])[:k-2]
            print(temp1)
            print(temp2)
            temp1.sort()
            temp2.sort()
            if temp1 == temp2:
                superSet.append(frequentlySet[i] | frequentlySet[j])
    
    return superSet

#选择频繁项集的程序
#最小支持度默认为0.5
def aprioriProcess(dataSet,minSupport = 0.5):
   
    #创建初始的项集
    initItemSet = createInitialSet(dataSet)
    #查找出频繁项集
    initFrequentlySet,SupportFrequently = searchFrequent(\
        dataSet,initItemSet,minSupport)
    frequentlySet = [initFrequentlySet]
    print(frequentlySet)
    k = 2
    #依次对之进行检查
    while len(frequentlySet[k-2]) > 0:
        #形成超集
        print('k=',k)
        Superset = createSuperSet(frequentlySet[k-2],k)
        #查找出超集的频繁项集
        FrequentlySuperset,support = searchFrequent(dataSet,Superset,minSupport)
        frequentlySet.append(FrequentlySuperset)
        SupportFrequently.update(support)
        k += 1
    return frequentlySet,SupportFrequently

if __name__ == '__main__':
    print('查找频繁项集')
    
    #dataSet = [[1,3,4],[2,3,5],[1,2,3,5],[2,5]]
    dataSet = dataSE.extractData()
    frequentlySet,SupportFrequently = aprioriProcess(dataSet,0.3)
    print(frequentlySet)
    print(SupportFrequently)





        
