import snap, networkx as nx 
import os, sys

path1 = os.path.join(os.getcwd(), sys.argv[1], "EgoNet","Article",'Article.graph')
FIn = snap.TFIn(path1)
G = snap.TNGraph.Load(FIn)

path2 = os.path.join(os.getcwd(), sys.argv[1], "EgoNet","Article",'Article.csv')
G1 = nx.read_edgelist(path2,delimiter=' ',nodetype=str)

file = open(os.path.join(os.getcwd(), sys.argv[1],"EgoNet","Article",'IndegreeAndOutdegree.csv'),"w")
for NI in G.Nodes():
		file.write(str(NI.GetId()) + ',' + str(NI.GetOutDeg()) +  ',' + str(NI.GetInDeg()) + '\n')
file.close()
