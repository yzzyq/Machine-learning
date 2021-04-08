from astropy.io import fits
import os


def outputFilename(location_name):
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
       #one_file.append(location_name)
       file_charact.append(one_file)
   os.chdir(os.pardir)
   return file_charact

def dataNorm(files_charact):
   for i in range(len(files_charact)):
      maxData = max(files_charact[i])
      minData = min(files_charact[i])
      lenData = maxData - minData
      for j in range(len(files_charact[i])):
         temp = files_charact[i][j] - minData
         files_charact[i][j] = temp / lenData

def extractData():       
   location_name = 'feafits'
   file_charact_fea = outputFilename(location_name)
  
   location_name = 'nofeafits'
   file_charact_nofea = outputFilename(location_name)
   dataNorm(file_charact_fea)
   dataNorm(file_charact_nofea)
   
   labelSet = [x for x in range(3600)]
   file_charact_fea[1:1] = file_charact_nofea
   
   return file_charact_fea


if __name__ == '__main__':
   dataSet = extractData()
   print(dataSet)
   







