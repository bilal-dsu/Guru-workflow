# Authors Bilal Hayat Butt, Sufyan Faizi
# Description The code is used to create collaboration network from authors extracted from 'Extraction.py'
# Collaboration network csv is created from the below code, which then converts into binary graph and hash files which is used for further analysys

import csv, snap,sys,os


list1 = []
list2 = []
list3 = []
Tuple = ('' , '')
path = os.path.join(os.getcwd(), sys.argv[5],sys.argv[4]) 
if not os.path.exists(path): #check if folder already exist, if it doesn't then create it
    os.makedirs(path)

path = os.path.join(os.getcwd(), sys.argv[5],sys.argv[4], sys.argv[1]+'.csv') # Collaboration network path for dumping data
file = open(path , 'w')

path2 = os.path.join(os.getcwd(), sys.argv[5], sys.argv[2]+'.csv')
with open(path2 , 'r') as data:
		reader = csv.reader(data , delimiter = ',')
		for row in reader:
				row.pop(0)
				list1 = list2 = row
				for Author in list1:
						for Collab in list2:
								if Author != Collab:
										Tuple = (Author , Collab)
										Tuple_reverse = (Collab , Author)
										if Tuple not in list3:
												list3.append(Tuple)
												list3.append(Tuple_reverse)
												file.write(str(Tuple) + '\n')
file.close()

fread = open(path , 'r')
data = fread.read()
data = data.replace(" " , "_")
data = data.replace("'" , "")
data = data.replace(")" , "")
data = data.replace("(" , "")
data = data.replace("," , " ")
fread.close()


fwrite = open(path , 'w')
fwrite.write(data)
fwrite.close()

#Save Author Collaboration Network as binary
mapping = snap.TStrIntSH()
LoadedGraph = snap.LoadEdgeListStr(snap.PUNGraph, path ,0,1,mapping)
path3 = os.path.join(os.getcwd(), sys.argv[5],sys.argv[4], sys.argv[3]+'.graph')
FOut = snap.TFOut(path3)
LoadedGraph.Save(FOut)
FOut.Flush()
path4 = os.path.join(os.getcwd(), sys.argv[5],sys.argv[4], sys.argv[3]+'.hash')
FOut = snap.TFOut(path4)
mapping.Save(FOut)
FOut.Flush()
