# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 22:43:36 2019

@author: Hp
"""
import snap,csv,os,sys

path1 = os.path.join(os.getcwd(),sys.argv[1],"EgoNet","Article","Article.graph")
path2 = os.path.join(os.getcwd(),sys.argv[1],"EgoNet","Article","Article.hash")

FIn1 = snap.TFIn(path2)
mapping = snap.TStrIntSH (FIn1)

FIn = snap.TFIn(path1)
G = snap.TNGraph.Load(FIn)

path3 = os.path.join(os.getcwd(),sys.argv[1],"EgoNet","Author Citation Network")
if not os.path.exists(path3): #check if folder already exist, if it doesn't then create it
    os.makedirs(path3)
    
path4 = os.path.join(path3,'AuthorCitationNetwork.csv')

Author_Citation_file = open(path4 , 'w')
#Create Author Citation Network
path5 = os.path.join(os.getcwd(),sys.argv[1],"EgoNet","DOI_AuthorCSEgoNet.csv")
for Edges in G.Edges():
	with open(path5 , 'r') as DOI_Author_file:
		doi_author = csv.reader(DOI_Author_file , delimiter = ',')
		for auth in doi_author:
			srcDOI = mapping.GetKey(Edges.GetSrcNId())
			destDOI = mapping.GetKey(Edges.GetDstNId())  
				
			if srcDOI == auth[0]:
				citingAuth = auth 
				del citingAuth[0]

			if destDOI == auth[0]: 
				citedAuth = auth
				del citedAuth[0]
					
			
		for ctngA in citingAuth:
			for ctdA in citedAuth:
				Author_Citation_file.write(ctngA + ' ' + ctdA + ',' + '\n')
			

Author_Citation_file.close()


try:
        #Create Article Citation Network Graph(binary)
        mapping = snap.TStrIntSH()
        G=snap.LoadEdgeListStr(snap.PNGraph, path4, 0, 1, mapping)
        newpath4 = os.path.join(path3, 'AuthorCitationNetwork.graph')
        FOut = snap.TFOut(newpath4)
        G.Save(FOut)
        FOut.Flush()
        path5 =os.path.join(path3, 'AuthorCitationNetwork.hash')
        FOut = snap.TFOut(path5)
        mapping.Save(FOut)
        FOut.Flush()
except:
        print("Graph Files Not Created")
