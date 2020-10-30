import csv
import time
import snap
import os,sys
import pandas as pd
start = time.time()


list1 = []
list2 = []
list3 = []
Tuple = ('' , '')

path = os.path.join(os.getcwd(),sys.argv[1],"EgoNet","Collaboration Network")
if not os.path.exists(path): #check if folder already exist, if it doesn't then create it
    os.makedirs(path)

path1 = os.path.join(path,'CollaborationNetwork.csv') 
pathtemp = os.path.join(path,'CollaborationNetworkTemp.csv')
chunksize = 100000

file = open(pathtemp , 'w')

path2 = os.path.join(os.getcwd(),sys.argv[1],"EgoNet","DOI_AuthorCSEgoNet.csv")

with open(path2 , 'r') as data:
	reader = csv.reader(data , delimiter = ',')
	for row in reader:
		row.pop(0)
		list1 = row
		list2 = row
		for Author in list1:
			for Collab in list2:
				if Author != Collab:
					Tuple = (Author , Collab)
					#Tuple_reverse = (Collab , Author)
					#if Tuple not in list3:
					list3.append(Tuple)
					#list3.append(Tuple_reverse)
					file.write(str(Tuple) + '\n')

file.close()

i=1
for df in pd.read_csv(pathtemp, chunksize=chunksize, iterator=True):
        df = df.replace({"'":''}, regex=True)
        df = df.replace({"\)":''}, regex=True)
        df = df.replace({"\(":''}, regex=True)
        df = df.replace({",":''}, regex=True)
        df.to_csv(path1,sep = ' ', mode = 'ab', index = None, header=False)
        i+=1


try:
        mapping = snap.TStrIntSH()
        LoadedGraph = snap.LoadEdgeListStr(snap.PUNGraph,path1, 0, 1, mapping)
        path3 = os.path.join(path, "CollaborationNetwork.graph")
        FOut = snap.TFOut(path3)
        LoadedGraph.Save(FOut)
        FOut.Flush()

        path3 = os.path.join(path, "CollaborationNetwork.Hash")
        FOut = snap.TFOut(path3)
        mapping.Save(FOut)
        FOut.Flush()
except:
        print("Graph Files Not Created")
