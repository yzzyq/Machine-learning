import generalTool as tool
import numpy as np
#SMO算法
#选取俩个a的值，一个不满足就行了。
#就是将不满足的KKT条件，变成在KKT范围内的，因为肯定在KKT范围内取值
#1.先选取一个ai，计算它的误差，查看是否满足KKT条件(是否被优化)
#2.满足条件，随机选择另外一个aj，再计算它的误差
#3.KKT条件是（0，C），并且值也在ai和aj的函数中，对之进行约束
#4.下面就是求新的ai的值了，根据是ai新和旧的公式
#5.先计算那个分母，查看它的值
#6.根据公式计算出新的值，优化幅度不大的话，可以结束，进行下一伦
#7.计算出另外一个aj的新值
#8.计算出b的值
#9.如果已经没有被优化的次数超过了限制次数，说明不用优化了

#dataSet数据集  labelSet分类出的类别  C软间隔     maxNum最大循环次数   toler容错率
def smoSimple(dataSet,labelSet,C,maxNum,toler):
    dataMatrix = np.mat(dataSet)
    labelMat = np.mat(labelSet).transpose()
    b = 0
    #循环次数
    num = 0
    m,n = np.shape(dataMatrix)
    #权值
    alphas = np.mat(np.zeros((m,1)))
    while num < maxNum:
        change = 0
        #依次选择进行优化
        for i in range(m):
            #带入公式中计算出结果
            result = float(np.multiply(alphas,labelMat).T*\
                           (dataMatrix*dataMatrix[i,:].T)) + b
##            print(i,result)
##            print(np.shape(np.multiply(alphas,labelMat).T))
##            print(np.shape(dataMatrix*dataMatrix[i,:].T))
##            print(np.shape(np.multiply(alphas,labelMat).T*\
##                           (dataMatrix*dataMatrix[i,:].T)))
            error = result - float(labelMat[i])
            #查看是否满足KKT条件
##            print('label',labelMat[i])
##            print('error',error)
            if ((labelMat[i]*error < -toler) and (alphas[i] < C)) \
               or ((labelMat[i]*error > toler) and (alphas[i] > 0)): 
                 #查找出aj,也就是第二个参数 
                second = tool.selectRandom(i,m)
                fxiSecond = float(np.multiply(alphas,labelMat).T*\
                                  (dataMatrix*dataMatrix[second,:].T)) + b
                errorSecond = fxiSecond - float(labelMat[second])
                #进行深拷贝，之后要进行比较
                first = alphas[i].copy()
                secondAlphas = alphas[second].copy()
                #它们限制在一个范围中,这是因为它们是一个函数的关系
                if labelMat[i] != labelMat[second]:
                    #下限  
                    l = max(0,alphas[second] - alphas[i])
                    #上限
                    h = min(C,C + alphas[second] - alphas[i])
                else:
                    #下限
                    l = max(0,alphas[second] + alphas[i])
                    #上限
                    h = min(C,alphas[second] + alphas[i] - C)
                #开始求优化解
                optimiz = 2.0*(dataMatrix[i,:]*dataMatrix[second,:].T) - \
                          (dataMatrix[i,:]*dataMatrix[i,:].T) -\
                          (dataMatrix[second,:]*dataMatrix[second,:].T)
                #print('opt',optimiz)
                if optimiz >= 0:
                    #print('optimiz >= 0')
                    continue
                alphas[second] -= labelMat[second]*(error - errorSecond)/optimiz
                alphas[second] = tool.restrictRange(alphas[second],h,l)
                #print(alphas[second])
                if abs(alphas[second] - secondAlphas) < 0.0000001:
                    #print('优化力度太小')
                    continue
                alphas[i] += labelMat[i]*labelMat[second]*(secondAlphas - alphas[second]) 
                #print('first',alphas[i]) 
                #开始更新b值
                b1 = b - error - labelMat[i]*(alphas[i] - first)*\
                     dataMatrix[i,:]*dataMatrix[i,:].T - \
                     labelMat[second]*(alphas[second] - secondAlphas)*\
                     dataMatrix[i,:]*dataMatrix[second,:].T
                b2 = b - errorSecond - labelMat[i]*(alphas[i] - first)\
                     *dataMatrix[i,:]*dataMatrix[second,:].T - \
                     labelMat[second]*(alphas[second] - secondAlphas)*\
                     dataMatrix[second,:]*dataMatrix[second,:].T
                #print('b1',b1)
                #print('b2',b2)
                #满足0，C的a，根据这个a求出来的b比较准确
                if 0 < alphas[i] and alphas[i] < C:
                    b = b1
                elif 0 < alphas[second] and alphas[second] < C:
                    b = b2
                else:
                    b = (b1 + b2) / 2.0
                change += 1
                #print('迭代次数：%d,选中的参数:%d,优化改变次数：%d' %\
                      #(num,i,change))
        if change == 0:
            num += 1
        else:
            num = 0
        #print('迭代次数:%d' % num)
    return b,alphas
