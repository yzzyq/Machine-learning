import createFPgrowth as createFP
#从树中查找频繁项集
def mineTree(reTree,headerTable,minSup,preFix,freqItem):
    print('headerTable:',headerTable)
    print('=======================================')
    items = [v[0] for v in sorted(headerTable.items(),key = lambda p:p[1][0])]
    for basePat in items:
        newFreqent = preFix.copy()
        newFreqent.add(basePat)
        print('newFreqent:',newFreqent)
        freqItem.append(newFreqent)
        print('freqItem:',freqItem)
        #找出所有的前缀路径
        condPatBase = findPrefixPath(basePat,headerTable[basePat][1])
        print("condPatBase:",condPatBase)
        myCondTree,myHeader = createFP.createTree(condPatBase,minSup)
        if myHeader != None:
            mineTree(myCondTree,myHeader,minSup,newFreqent,freqItem)

#找出条件模式基
def findPrefixPath(basePat,treeNode):
    condPat = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode,prefixPath)
        if len(prefixPath) > 1:
            condPat[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPat

def ascendTree(treeNode,prefixPath):
    if treeNode.parent != None:
        prefixPath.append(treeNode.name)
        ascendTree(treeNode.parent,prefixPath)

if __name__ == '__main__':
    dataSet = [['r','z','h','j','p'],['z'],['z','y','x','w','v','u','t','s'],\
               ['r','x','n','o','s'],['y','r','x','z','q','s','p'],\
               ['y','z','x','e','q','s','t','m']]
    dataDict = createFP.crateInitData(dataSet)
    print(dataDict)
    reTree,headerTable = createFP.createTree(dataDict,3)
    reTree.disp()
    myFreqList = []
    mineTree(reTree,headerTable,3,set([]),myFreqList)
    print(myFreqList[0])
    

        
