#存储全部的全局变量
#存储枝平衡因子、叶平衡因子、空间阈值
def init():
    global globalDict
    globalDict = {}

def setValue(name,value):
    globalDict[name] = value

def getValue(name,defValue=None):
    try:
        return globalDict[name]
    except KeyError:
        return defValue
