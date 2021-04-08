import apriori
import assoicationRules
import dataSetExract

dataSet = dataSetExract.extractData()
frequentlySet,SupportFrequently = apriori.aprioriProcess(dataSet,0.3)
print(frequentlySet)
rule = assoicationRules.generateRules(frequentlySet,SupportFrequently,minConfidence = 0.3)
print(rule)

