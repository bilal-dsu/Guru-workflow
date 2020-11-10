# Authors Bilal Hayat Butt, Sufyan Faizi
# Description The code loads the edgelist created from 'Edge_List.py' and create two binary files, graph and hash file.
# graph file which contains the directed citation network of COCI
# hash file which maps the integer node label to respective DOI

import snap #pip install snap-stanford
import sys,os

#new path for data to be dumped and loaded.
path = os.path.join(os.getcwd(), sys.argv[4], sys.argv[1]+'.csv')

NodeList = snap.TStrIntSH()
DOI = snap.LoadEdgeListStr(snap.PNGraph, path, 0, 1, NodeList)

path = os.path.join(os.getcwd(), sys.argv[4], sys.argv[2]+'.graph')
FOut = snap.TFOut(path)
DOI.Save(FOut)
FOut.Flush()

path = os.path.join(os.getcwd(), sys.argv[4], sys.argv[3]+'.hash')
FOut = snap.TFOut(path)
NodeList.Save(FOut)
FOut.Flush()
