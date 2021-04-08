import apriori

#计算并选择满足最小置信度
def calc(items,eachSet,SupportFrequently,rule,minConfidence):
    rulesTmple = []
    for data in eachSet:
        #求出置信度
        confident = SupportFrequently[items] / SupportFrequently[items - data]
        if confident >=  minConfidence:
            print(list(items - data),'--->',data)
            rulesTmple.append(data)
            rule.append((items-data,data,confident))
            print((items-data,data,confident))     
    return rulesTmple

#组合项集并且选择出
def combination(items,eachSet,SupportFrequently,rule,minConfidence):
    m = len(eachSet[0])
    if len(items) > m + 1:
        superSet = apriori.createSuperSet(eachSet,m+1)
        superSet = calc(items,superSet,SupportFrequently,rule,minConfidence)
        if len(superSet) > 1:
            combination(items,superSet,SupportFrequently,rule,minConfidence)
        
#从频繁项集中找出关联规则
def generateRules(frequentlySet,SupportFrequently,minConfidence = 0.7):
    lenData = len(frequentlySet)
    rule = []
    for i in range(1,lenData):
        for items in frequentlySet[i]:
            #之后能够好处理，先处理一个每个项集
            eachSet = [frozenset([item]) for item in items]
            if i > 1:
                #多于俩个元素就要进行组合
                combination(items,eachSet,SupportFrequently,rule,minConfidence)
            else:
                #俩个元素就直接计算
                calc(items,eachSet,SupportFrequently,rule,minConfidence)
    return rule


if __name__ == '__main__':
    print('查找频繁项集')
    dataSet = [[1,3,4],[2,3,5],[1,2,3,5],[2,5]]
    frequentlySet,SupportFrequently = apriori.aprioriProcess(dataSet,0.5)
    print(frequentlySet)
    rule = generateRules(frequentlySet,SupportFrequently,minConfidence = 0.5)
    print(rule)
    

