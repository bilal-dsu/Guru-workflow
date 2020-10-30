import snap ,  networkx as nx
import os, sys

path1 = os.path.join(os.getcwd(), sys.argv[1], "EgoNet","Author Citation Network",'AuthorCitationNetwork.hash')
FIn1 = snap.TFIn(path1)
mapping = snap.TStrIntSH (FIn1)

path1 = os.path.join(os.getcwd(), sys.argv[1],"EgoNet","Author Citation Network",'AuthorCitationNetwork.graph')
FIn = snap.TFIn(path1)
G = snap.TNGraph.Load(FIn)

#Degree Centrality
file = open(os.path.join(os.getcwd(), sys.argv[1],"EgoNet","Author Citation Network",'Author_Citation_DegCen.csv') , 'w',errors='ignore')
    
InDegV = snap.TIntPrV()
snap.GetNodeInDegV(G, InDegV)
    
OutDegV = snap.TIntPrV()
snap.GetNodeOutDegV(G, OutDegV)
file.write('Authors' +','+ 'IndegCentr' +','+ 'IndegCentr' + '\n')
for (item1 , item2) in zip(InDegV , OutDegV):
    file.write(mapping.GetKey(item1.GetVal1()) + ',' + str(item1.GetVal2())+ ',' + str(item2.GetVal2())  + '\n')
file.close()


#Betweenness Centrality
file = open(os.path.join(os.getcwd(), sys.argv[1],"EgoNet","Author Citation Network",'Author_Citation_BetweensCen.csv') , 'w',errors='ignore')
file.write('Authors' +','+ 'BetweennessCent' + '\n')

Nodes = snap.TIntFltH()
Edges = snap.TIntPrFltH()
snap.GetBetweennessCentr(G, Nodes, Edges, 1.0)
for node in Nodes:
    file.write(str(mapping.GetKey(node)) +','+ str(Nodes[node]) + '\n')
file.close()

#Eigen Centrality
file = open(os.path.join(os.getcwd(), sys.argv[1],"EgoNet","Author Citation Network",'Author_Citation_EigenCen.csv') , 'w',errors='ignore')
file.write('Authors' +','+ 'EigenCen' + '\n')


graph  = nx.read_edgelist(os.path.join(os.getcwd(), sys.argv[1],"EgoNet","Author Citation Network",'AuthorCitationNetwork.csv'),nodetype=str , delimiter=' ')
g = nx.DiGraph(graph)

centrality = nx.eigenvector_centrality(g)
i=0
for node in centrality:
    file.write(str(node) +','+ str(centrality[node]) + '\n')
    i=i+1
file.close()
