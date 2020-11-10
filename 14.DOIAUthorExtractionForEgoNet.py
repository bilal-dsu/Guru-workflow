# Authors Bilal Hayat Butt, Talha Aslam, Sufyan Faizi
# Description
import json, os,sys,snap

path = os.path.join(os.getcwd(),sys.argv[1],"EgoNet","DOI_AuthorCSEgoNet.csv")
doi_author_file = open(path , 'w')

Graphpath = os.path.join(os.getcwd(),sys.argv[1],"EgoNet","Article","Article.graph")
FIn = snap.TFIn(Graphpath)
G = snap.TNGraph.Load(FIn)
for Jsonfiles in range(G.GetNodes()):

    try:
        path2 = os.path.join(os.getcwd(),sys.argv[1],"EgoNet","CSEgoNetDump","M"+str(Jsonfiles)+".json")
        with open(path2 , 'r') as JsonData:
            Data = json.load(JsonData)
            
    except IOError:
        pass

    try:
        Author_Name = ''
        for records in Data['message']['author']:
            dic = {}
            dic = dict(records.items())
            Author_Name = Author_Name + ',' + unicode(dic.get('given')).encode("utf-8") + ' ' + unicode(dic.get('family')).encode("utf-8")
            
        doi_author_file.write(unicode(Data['message']['DOI']).encode("utf-8") +  str(Author_Name) + '\n')
    except KeyError:
        pass
doi_author_file.close()
fread = open(path , 'r')
data = fread.read()
data = data.replace(' ' , '_')
fread.close()
fwrite = open(path , 'w')
fwrite.write(data)
fwrite.close() 
