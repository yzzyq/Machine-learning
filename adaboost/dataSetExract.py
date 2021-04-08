from astropy.io import fits
import os
import random
import copy


def outputFilename(location_name,classFile):
   os.chdir(location_name)
   list_file = os.listdir(os.curdir)
   file_charact = []
   for file in list_file:
       one_file = []
       dfu = fits.open(file)
       infoHeader = dfu[0].header
       #num = infoHeader['NAXIS1']
       infoData = dfu[0].data
       for i in range(3600): 
         one_file.append(float(infoData[0][i]))
       #类别
       one_file.append(float(classFile))
       file_charact.append(one_file)
   os.chdir(os.pardir)
   return file_charact

def extractData():       
   location_name = 'feafits'
   file_charact_fea = outputFilename(location_name,1)
  
   location_name = 'nofeafits'
   file_charact_nofea = outputFilename(location_name,-1)
  
   labelSet = []
   file_charact_fea[1:1] = file_charact_nofea

   #切分数据，90%是训练数据，10%是测试数据
   length = len(file_charact_fea)
   i = 0
   #训练集
   trainData = []
   while i < length*0.9:
      index = random.randrange(len(file_charact_fea))
      data = copy.deepcopy(file_charact_fea[index])
      trainData.append(data)
      del file_charact_fea[index]
      i += 1
   
   for i in range(len(trainData)):
      labelSet.append(trainData[i][-1])
      del trainData[i][-1]
   return trainData,file_charact_fea,labelSet


if __name__ == '__main__':
   trainData,exeData,labelSet = extractData()
   print(len(trainData),len(labelSet))






