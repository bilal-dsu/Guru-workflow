import snap ,os, pandas as pd,sys

srcNode = ''
dstNode = ''
i=0

print("Reading Graph Files")
FIn1 = snap.TFIn(sys.argv[1]+".hash")
COCIMapping = snap.TStrIntSH (FIn1)

FIn = snap.TFIn(sys.argv[2]+".graph")
COCIGraph = snap.TNGraph.Load(FIn)

path = os.path.join(os.getcwd(), sys.argv[3], sys.argv[4], sys.argv[5]+'.csv')
CSMapping = snap.TStrIntSH()
CSGraph = snap.LoadEdgeListStr(snap.PNGraph, path, 0, 1, CSMapping)

path1 = os.path.join(os.getcwd(),sys.argv[3],"EgoNet","Article")

os.makedirs(path1)

path2 = os.path.join(path1,'Article.csv')

file = open(path2,'w')
for CSNode in CSGraph.Nodes():
        COCINode = COCIGraph.GetNI(CSNode.GetId())
        #COCINode = CSNode
        for Id in COCINode.GetOutEdges():
            print("edge (%s %s)" % (COCIMapping.GetKey(COCINode.GetId()), COCIMapping.GetKey(Id)))
            srcNode = COCIMapping.GetKey(COCINode.GetId())
            dstNode = COCIMapping.GetKey(Id)
            file.write(srcNode + ' ' + dstNode  + '\n')

        for Id in COCINode.GetInEdges():
            print("edge (%s %s)" % (COCIMapping.GetKey(COCINode.GetId()), COCIMapping.GetKey(Id)))
            srcNode = COCIMapping.GetKey(COCINode.GetId())
            dstNode = COCIMapping.GetKey(Id)
            file.write(srcNode + ' ' + dstNode  + '\n')

file.close()
try:
        path1 = os.path.join(os.getcwd(),sys.argv[3],"EgoNet","Article","Article.csv")

        #Create CSEgoNet Graph(binary)
        mapping = snap.TStrIntSH()
        G=snap.LoadEdgeListStr(snap.PNGraph, path1, 0, 1, mapping)
        newpath4 = os.path.join(os.getcwd(), sys.argv[3],"EgoNet","Article", 'Article.graph')
        FOut = snap.TFOut(newpath4)
        G.Save(FOut)
        FOut.Flush()
        path5 =os.path.join(os.getcwd(), sys.argv[3], "EgoNet","Article", 'Article.hash')
        FOut = snap.TFOut(path5)
        mapping.Save(FOut)
        FOut.Flush()
except:
        print("Graph Files Not Created")