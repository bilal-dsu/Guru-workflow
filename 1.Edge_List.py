"""
Created on Sun Nov 24 2019
@author: Bilal Hayat Butt, Sufyan Faizi
@Description: The code converts COCI data csv to edgelist csv which contains citing and cited columns.

"""

import pandas as pd #pip install pandas
import sys,os

path = os.path.join(os.getcwd(), sys.argv[2])
DOIcsv = os.path.join(path, sys.argv[1])+'.csv'

numFiles = []
fileNames = os.listdir(path)
for fileNames in fileNames:
  if fileNames.endswith(".csv"):
    numFiles.append(fileNames)

for f in numFiles:
  data = path+f
  i = 1
  for df in pd.read_csv(data, usecols=['citing','cited'], chunksize=chunksize, iterator=True):
    df = df.replace({'\n':''}, regex=True)
    df = df.replace({'"':''}, regex=True)
    df.to_csv(DOIcsv,sep = ' ', mode = 'ab', index = None, header=False)
    i+=1
