"""

Created on Sun Nov 24 2019
@author: Bilal Hayat Butt, Sufyan Faizi
@Description: The code is used to apply centrality analysis on collaboration network
First, collaboration network graph is loaded in memory
Second, SNAP and Netoworkx python API's were used to calculate the scores of below centrality measures
Degree centrality
Eigen centrality
Betweness, closeness and farness centrality
Lastly, the scores were populated in csv

"""

# Authors Bilal Hayat Butt, Sufyan Faizi
# Description 
import os, sys
import snap, networkx as nx


path1 = os.path.join(os.getcwd(), sys.argv[1],sys.argv[2], sys.argv[3]+'.hash')
FIn = snap.TFIn(path1)
mapping = snap.TStrIntSH (FIn)

path1 = os.path.join(os.getcwd(), sys.argv[1],sys.argv[2], sys.argv[3]+'.graph')
FIn = snap.TFIn(path1)
UGraph = snap.TUNGraph.Load(FIn)


file = open(os.path.join(os.getcwd(), sys.argv[1],sys.argv[2], 'Collaboration_DegCent.csv') , 'w', errors='ignore')

file.write('Author_Name' +',' + 'Degree_Centrality' +'\n')

for NI in UGraph.Nodes():
		DegCentr = snap.GetDegreeCentr(UGraph, NI.GetId())
		file.write(mapping.GetKey(NI.GetId()) +',' + str(DegCentr) +'\n')
file.close()

PRankH = snap.TIntFltH()
file = open( os.path.join(os.getcwd(), sys.argv[1],sys.argv[2], 'Collaboration_EigenCent.csv'), 'w', errors='ignore')

NIdEigenH = snap.TIntFltH()
snap.GetEigenVectorCentr(UGraph, NIdEigenH , 1e-8, 1000)
snap.GetPageRank(UGraph, PRankH, 0.85, 1e-8, 1000)

file.write('Author_Name' +',' + 'Eigen_Centrality' +'\n')
for item in NIdEigenH:
    file.write(mapping.GetKey(item)  + ',' + str(NIdEigenH[item]) + '\n')
file.close()


file = open(os.path.join(os.getcwd(), sys.argv[1],sys.argv[2], 'Collaboration_BetweenCent.csv') , 'w', errors='ignore')


Nodes, Edges  = snap.TIntFltH(), snap.TIntPrFltH()
snap.GetBetweennessCentr(UGraph, Nodes, Edges, 1.0 , False)
file.write('Author_Name' +',' + 'Betweenness_Centrality' +'\n')
for node in Nodes:
    file.write(mapping.GetKey(node) +','+ str(Nodes[node]) + '\n')
file.close()


file = open(os.path.join(os.getcwd(), sys.argv[1],sys.argv[2], 'Collaboration_ClosenessCent.csv') , 'w', errors='ignore')
file.write('Author_Name' +',' + 'Closeness_Centrality' +'\n')
for NI in UGraph.Nodes():
    CloseCentr = snap.GetClosenessCentr(UGraph, NI.GetId())
    file.write(mapping.GetKey(NI.GetId()) +','+ str(CloseCentr) + '\n')
file.close()


file = open(os.path.join(os.getcwd(), sys.argv[1],sys.argv[2], 'Collaboration_FarenessCent.csv') , 'w', errors='ignore')
file.write('Author_Name' +',' + 'Fareness' +'\n')
for NI in UGraph.Nodes():
    FarCentr = snap.GetFarnessCentr(UGraph, NI.GetId())
    file.write(mapping.GetKey(NI.GetId()) +','+ str(FarCentr) + '\n')
file.close()

