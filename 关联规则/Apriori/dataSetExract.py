from astropy.io import fits
import os


def outputFilename(location_name,numType):
   os.chdir(location_name)
   list_file = os.listdir(os.curdir)
   file_charact = []
   for file in list_file:
       one_file = []
       dfu = fits.open(file)
       infoHeader = dfu[0].header
       #num = infoHeader['NAXIS1']
       infoData = dfu[0].data
       #maxData = max(infoData[0])
       #minData = min(infoData[0])
       #maxToMin = maxData - minData
       num = 0
       temp = 0
       for i in range(3600):
          if num <= 100:
             temp += infoData[0][i]
             num += 1
          else:
             one_file.append(temp)
             num = 0
             temp = 0
          #temp = infoData[0][i] - minData
          #one_file.append(temp / maxToMin)
       #类别
       one_file.append(numType)
       file_charact.append(one_file)
   os.chdir(os.pardir)
   return file_charact

def extractData():       
   location_name = 'feafits'
   file_charact_fea = outputFilename(location_name,1)
   #print(len(file_charact[-1]))

   location_name = 'nofeafits'
   file_charact_nofea = outputFilename(location_name,2)
   dataNorm(file_charact_fea)
   dataNorm(file_charact_nofea)

   
   dataToDiscrete(file_charact_fea)
   dataToDiscrete(file_charact_nofea)
   
  
##   labelSet = [x for x in range(3600)]
   file_charact_fea[1:1] = file_charact_nofea
   
   return file_charact_fea

#对数据进行定值
def dataToDiscrete(file_charact):
   for i in range(len(file_charact)):
      k = 0
      for j in range(len(file_charact[i])-1):
##         if file_charact[i][j] < 0.5:
##            file_charact[i][j] = 1 + k    
##         else:
##            file_charact[i][j] = 2 + k
         file_charact[i][j] = int(file_charact[i][j]*10) + k
         k += 10
        
      #print(k)
      file_charact[i][len(file_charact[i])-1] = k + \
                                    file_charact[i][len(file_charact[i])-1]

      
            
##         temp = int(file_charact[i][j]*10)
##         file_charact[i][j] = temp + k
##         k += 10

def dataNorm(files_charact):
   for i in range(len(files_charact)):
      maxData = max(files_charact[i])
      minData = min(files_charact[i])
      lenData = maxData - minData
      for j in range(len(files_charact[i])):
         temp = files_charact[i][j] - minData
         files_charact[i][j] = temp / lenData
         
  
   


if __name__ == '__main__':
   location_name = 'feafits'
   file_charact = outputFilename(location_name,1)
   #print(len(file_charact[-1]))

   location_name = 'nofeafits'
   file_charact_nofea = outputFilename(location_name,2)
   dataNorm(file_charact)
   dataNorm(file_charact_nofea)
   print(file_charact)
   
   dataToDiscrete(file_charact)
   dataToDiscrete(file_charact_nofea)
   print(file_charact)
   #for file in file_charact:
   #   print(file[-1])
   #for file in file_charact_nofea:
   #   print(file[-1])

   
   
   





