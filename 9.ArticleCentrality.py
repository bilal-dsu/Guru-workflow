"""
Created on Sun Nov 24 2019
@author: Bilal Hayat Butt, Sufyan Faizi
@Description: The code is used centrality analysis in article citation network
First, article citation network graph is loaded,
Second, indegree and out degree centrality was calculated from article citation network

"""



import snap, networkx as nx 
import os, sys

path1 = os.path.join(sys.argv[4]+'.hash')
FIn1 = snap.TFIn(path1)
mapping = snap.TStrIntSH (FIn1)

path1 = os.path.join(os.getcwd(), sys.argv[1], sys.argv[2],sys.argv[3]+'.graph')
FIn = snap.TFIn(path1)
G = snap.TNGraph.Load(FIn)

path2 = os.path.join(os.getcwd(), sys.argv[1], sys.argv[2],sys.argv[3]+'.csv')
G1 = nx.read_edgelist(path2,delimiter=' ',nodetype=str)

file = open(os.path.join(os.getcwd(), sys.argv[1],sys.argv[2],'IndegreeAndOutdegree.csv'),"w")
file.write('DOI' +','+ 'Out_Degree' +','+ 'In_Degree' + '\n')
for NI in G.Nodes():
		file.write(mapping.GetKey(NI.GetId()) + ',' + str(NI.GetOutDeg()) +  ',' + str(NI.GetInDeg()) + '\n')
file.close()

'''
file = open(os.path.join(os.getcwd(), sys.argv[1],sys.argv[2],'katz.csv'),"w")
centrality = nx.katz_centrality(G1 , normalized=True , tol=1e-06)

file.write('DOI' +','+ 'KatzCentr' + '\n')

for n,c in sorted(centrality.items()):
	file.write(str(n) + ',' + str(c) + '\n')
file.close()
'''
