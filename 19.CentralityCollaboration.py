import os, sys
import snap, networkx as nx

path1 = os.path.join(os.getcwd(), sys.argv[1],"EgoNet","Collaboration Network","CollaborationNetwork.hash")
FIn = snap.TFIn(path1)
mapping = snap.TStrIntSH (FIn)

path1 = os.path.join(os.getcwd(), sys.argv[1],"EgoNet","Collaboration Network",'CollaborationNetwork.graph')
FIn = snap.TFIn(path1)
UGraph = snap.TUNGraph.Load(FIn)


file = open(os.path.join(os.getcwd(), sys.argv[1],"EgoNet","Collaboration Network", 'Collaboration_DegCent.csv') , 'w', errors='ignore')

for NI in UGraph.Nodes():
		DegCentr = snap.GetDegreeCentr(UGraph, NI.GetId())
		file.write(mapping.GetKey(NI.GetId()) +',' + str(DegCentr) +'\n')
file.close()

PRankH = snap.TIntFltH()
file = open( os.path.join(os.getcwd(), sys.argv[1],"EgoNet","Collaboration Network", 'Collaboration_EigenCent.csv'), 'w', errors='ignore')

NIdEigenH = snap.TIntFltH()
snap.GetEigenVectorCentr(UGraph, NIdEigenH , 1e-8, 1000)
snap.GetPageRank(UGraph, PRankH, 0.85, 1e-8, 1000)

for item in NIdEigenH:
    file.write(mapping.GetKey(item)  + ',' + str(NIdEigenH[item]) + '\n')
file.close()


file = open(os.path.join(os.getcwd(), sys.argv[1],"EgoNet","Collaboration Network", 'Collaboration_BetweenCent.csv') , 'w', errors='ignore')


Nodes, Edges  = snap.TIntFltH(), snap.TIntPrFltH()
snap.GetBetweennessCentr(UGraph, Nodes, Edges, 1.0 , False)
for node in Nodes:
    file.write(mapping.GetKey(node) +','+ str(Nodes[node]) + '\n')
file.close()


file = open(os.path.join(os.getcwd(), sys.argv[1],"EgoNet","Collaboration Network", 'Collaboration_ClosenessCent.csv') , 'w', errors='ignore')

for NI in UGraph.Nodes():
    CloseCentr = snap.GetClosenessCentr(UGraph, NI.GetId())
    file.write(mapping.GetKey(NI.GetId()) +','+ str(CloseCentr) + '\n')
file.close()


file = open(os.path.join(os.getcwd(), sys.argv[1],"EgoNet","Collaboration Network", 'Collaboration_FarenessCent.csv') , 'w', errors='ignore')

for NI in UGraph.Nodes():
    FarCentr = snap.GetFarnessCentr(UGraph, NI.GetId())
    file.write(mapping.GetKey(NI.GetId()) +','+ str(FarCentr) + '\n')
file.close()
