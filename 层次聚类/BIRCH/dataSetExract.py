from astropy.io import fits
import os
from sklearn.manifold import TSNE


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


def extractData():       
   location_name = 'feafits'
   file_charact_fea = outputFilename(location_name)
  
   location_name = 'nofeafits'
   file_charact_nofea = outputFilename(location_name)
  
   labelSet = [x for x in range(3600)]
   file_charact_fea[1:1] = file_charact_nofea
   tsne = TSNE(n_components = 2,init = 'pca',random_state = 0)
   result = tsne.fit_transform(file_charact_fea)
   return result


if __name__ == '__main__':
   dataSet = extractData()
   print(dataSet)
   







