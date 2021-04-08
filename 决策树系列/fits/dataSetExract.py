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
         one_file.append(infoData[0][i])
                
##       threeAver = sum(infoData[2][400:700])/300
##       negativeNum = 0
##       zeroNum = 0
##       for i in infoData[0][400:700]:
##           i = int(i)
##           if i < 0:
##               negativeNum += 1
##       for i in infoData[1][400:700]:
##           if i == 0:
##               zeroNum += 1
##       one_file.append(threeAver)
##       one_file.append(negativeNum) 
##       one_file.append(zeroNum)
       #类别
       one_file.append(location_name)
       file_charact.append(one_file)
   os.chdir(os.pardir)
   return file_charact

def extractData():       
   location_name = 'feafits'
   file_charact_fea = outputFilename(location_name)
  

   location_name = 'nofeafits'
   file_charact_nofea = outputFilename(location_name)
  
   labelSet = [x for x in range(3600)]
   file_charact_fea[1:1] = file_charact_nofea
   return file_charact_fea,labelSet





