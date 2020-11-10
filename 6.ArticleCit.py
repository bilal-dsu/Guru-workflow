# Authors Bilal Hayat Butt, Sufyan Faizi
# Description The code is used to create article citation network from DOI's extracted from 'DOIList.py'
# First it loads the COCI data graph and hash files created from 'SNAP_Binary.py'
# Second, the code creates vector of node id present in the csv which is created from 'DOIList.py' 
# Third, find the subgraph of created vector in graph file
# Fourth, create graph of article citation network 

import snap,csv,sys,os

#Load COCI Data
path = (sys.argv[1]+'.hash')
FIn1 = snap.TFIn(path)
mapping = snap.TStrIntSH (FIn1)

path2 = (sys.argv[2]+'.graph')
FIn = snap.TFIn(path2)
G = snap.TNGraph.Load(FIn)


V = snap.TIntV() #create Vector of nodeid
path3 = os.path.join(os.getcwd(), sys.argv[5], sys.argv[3]+'.csv')
with open(path3,'r') as Sci_DOI_List_file:
	data = csv.reader(Sci_DOI_List_file)
	for doi in data:
			NodeId = mapping.GetKeyId(doi[0])
			V.Add(NodeId)
				
Sci_DOI_List_file.close()
path = os.path.join(os.getcwd(), sys.argv[5],sys.argv[6] )
if not os.path.exists(path): #check if folder already exist, if it doesn't then create it
    os.makedirs(path)

SubGraph = snap.GetSubGraph(G, V) #Find Subgraph
path4 = os.path.join(os.getcwd(), sys.argv[5],sys.argv[6] , sys.argv[4] +'.csv')
file = open(path4,'w') #CSV of Article Citation
for EI in SubGraph.Edges():
	SrcDoi = mapping.GetKey(EI.GetSrcNId())
	DstDoi = mapping.GetKey(EI.GetDstNId())
	file.write(SrcDoi + ' ' + DstDoi  + '\n')
file.close()

#Create Article Citation Network Graph(binary)
#mapping = snap.TStrIntSH()
newpath4 = os.path.join(os.getcwd(), sys.argv[5],sys.argv[6], sys.argv[4]+'.graph')

FOut = snap.TFOut(newpath4)
SubGraph.Save(FOut)
FOut.Flush()

#path5 =os.path.join(os.getcwd(), sys.argv[5], sys.argv[6], sys.argv[4]+'.hash')
#FOut = snap.TFOut(path5)
#mapping.Save(FOut)
#FOut.Flush()


