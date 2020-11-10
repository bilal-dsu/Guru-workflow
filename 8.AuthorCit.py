# Authors Bilal Hayat Butt, Sufyan Faizi
# Description The code is used to create author citation network
# The code loads the graph of article citation network

import csv , time , snap, os, sys
#Load Article Citation Graph

path1 = os.path.join(sys.argv[7]+'.hash')
FIn1 = snap.TFIn(path1)
mapping = snap.TStrIntSH (FIn1)
path2 = os.path.join(os.getcwd(), sys.argv[5],sys.argv[4], sys.argv[1]+'.graph')
FIn = snap.TFIn(path2)
G = snap.TNGraph.Load(FIn)

path = os.path.join(os.getcwd(), sys.argv[5],sys.argv[6] )
if not os.path.exists(path): #check if folder already exist, if it doesn't then create it
    os.makedirs(path)

path3 = os.path.join(os.getcwd(), sys.argv[5],sys.argv[6], sys.argv[2]+'.csv')
file = open(path3 , 'w')
#Create Author Citation Network

		
for Edges in G.Edges():
	path4 = os.path.join(os.getcwd(), sys.argv[5], sys.argv[3]+'.csv')
	with open(path4 , 'r') as DOI_Author_file: doi_author = csv.reader(DOI_Author_file , delimiter = ',')
		srcDOI = mapping.GetKey(Edges.GetSrcNId())
		destDOI = mapping.GetKey(Edges.GetDstNId())  
			
		for auth in doi_author:
			
			if srcDOI == auth[0]:
				citingAuth = auth 
				del citingAuth[0]

			if destDOI == auth[0]:
				citedAuth = auth
				del citedAuth[0]		

		for ctngA in citingAuth:
			for ctdA in citedAuth:
				file.write(ctngA + ',' + ctdA + ',' + '\n')
		

file.close()
fread = open(path3,'r')
data  = fread.read()
data = data.replace(' ','_')
data = data.replace(',',' ')
fread.close()

fwrite = open(path3 , 'w')
fwrite.write(data)
fwrite.close()

#Create Author Citation Graph(binary)   	
			 
mapping = snap.TStrIntSH()

path = os.path.join(os.getcwd(), sys.argv[5],sys.argv[6], sys.argv[2]+'.csv')
G = snap.LoadEdgeListStr(snap.PNGraph, path , 0, 1, mapping)

path = os.path.join(os.getcwd(), sys.argv[5],sys.argv[6], sys.argv[2]+'.graph')
FOut = snap.TFOut(path)
G.Save(FOut)
FOut.Flush()

path = os.path.join(os.getcwd(), sys.argv[5],sys.argv[6], sys.argv[2]+'.hash')
FOut = snap.TFOut(path)
mapping.Save(FOut)
FOut.Flush()
