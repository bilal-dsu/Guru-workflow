# Authors Bilal Hayat Butt, Sufyan Faizi
# Description The code is used to apply centrality analysis on author citation network
# First, author citation graph is loaded in memory
# Second, SNAP and Netoworkx python API's were used to calculate the scores of below centrality measures
# Indegree and Outdegree centrality
# Eigen centrality
# Betweness centrality

import snap ,  networkx as nx
import os, sys

path1 = os.path.join(os.getcwd(), sys.argv[1], sys.argv[2],sys.argv[3]+'.hash')
FIn1 = snap.TFIn(path1)
mapping = snap.TStrIntSH (FIn1)

path1 = os.path.join(os.getcwd(), sys.argv[1], sys.argv[2],sys.argv[3]+'.graph')
FIn = snap.TFIn(path1)
G = snap.TNGraph.Load(FIn)

#Degree Centrality
file = open(os.path.join(os.getcwd(), sys.argv[1],sys.argv[2],'Author_Citation_DegCen.csv') , 'w',errors='ignore')
    
InDegV = snap.TIntPrV()
snap.GetNodeInDegV(G, InDegV)
    
OutDegV = snap.TIntPrV()
snap.GetNodeOutDegV(G, OutDegV)
file.write('Author_Name' +','+ 'In_Degree' +','+ 'Out_Degree' + '\n')
for (item1 , item2) in zip(InDegV , OutDegV):
    file.write(mapping.GetKey(item1.GetVal1()) + ',' + str(item1.GetVal2())+ ',' + str(item2.GetVal2())  + '\n')
file.close()


#Eigen Centrality
file = open(os.path.join(os.getcwd(), sys.argv[1],sys.argv[2],'Author_Citation_EigenCen.csv') , 'w',errors='ignore')

#g = nx.read_edgelist(os.path.join(os.getcwd(), sys.argv[1],sys.argv[2], sys.argv[3]+'.csv'),delimiter=' ', create_using=nx.DiGraph(), encoding = "latin-1")
#g = nx.DiGraph(graph)
PRankH = snap.TIntFltH()
#snap.GetEigenVectorCentr(G, NIdEigenH , 1e-8, 1000)
snap.GetPageRank(G, PRankH, 0.85, 1e-8, 1000)

file.write('Author_Name' +',' + 'Eigen_centrality' +'\n')
for item in PRankH:
    file.write(mapping.GetKey(item)  + ',' + str(PRankH[item]) + '\n')
file.close()
'''
centrality = nx.eigenvector_centrality(g)
i=0
for node in centrality:
    file.write(str(node) +','+ str(centrality[node]) + '\n')
    i=i+1
file.close()
'''
#Betweenness Centrality
file = open(os.path.join(os.getcwd(), sys.argv[1],sys.argv[2],'Author_Citation_BetweensCen.csv') , 'w',errors='ignore')
file.write('Author_Name' +','+ 'Betweenness_Centrality' + '\n')

Nodes = snap.TIntFltH()
Edges = snap.TIntPrFltH()
snap.GetBetweennessCentr(G, Nodes, Edges, 1.0)
for node in Nodes:
    file.write(str(mapping.GetKey(node)) +','+ str(Nodes[node]) + '\n')
file.close()
