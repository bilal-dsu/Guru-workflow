import requests
import json
import snap, urllib, imp, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import punctuation
import time, os, sys

path = os.path.join(os.getcwd(),sys.argv[1],"EgoNet","Article","Article.hash")
FIn1 = snap.TFIn(path)
mapping = snap.TStrIntSH(FIn1)

Graphpath = os.path.join(os.getcwd(),sys.argv[1],"EgoNet","Article","Article.graph")
FIn = snap.TFIn(Graphpath)
G = snap.TNGraph.Load(FIn)

print('Successfully Load Hash File')

path1 = os.path.join(os.getcwd(),sys.argv[1],"EgoNet","CSEgoNetDump")
os.mkdir(path1)

path2 = os.path.join(path1,"DOI_notfound.txt")

h=open(path2,'a')

var=0

for i in range(var , G.GetNodes()):
       
    try:
        s = mapping.GetKey(i)
        
        r = s.rstrip('.')

        response = urllib.urlopen("https://api.crossref.org/v1/works/" + r)
    

        data = json.loads(response.read())
        path5 = os.path.join(path1,'M'+str(i)+'.json')
        
        with open(path5, 'w') as k:
            json.dump(data,k)
        f=open('DOI_Id.txt','w')
        f.write('DOI_var =' + str(i))
       
    except ValueError as v:
        print('Value Error')
        time.sleep(600)

        try:
            path4 = os.path.join(path1,'M'+str(i)+'.json')
            response = urllib.urlopen("https://api.crossref.org/v1/works?" + r)
            data = json.loads(response.read())
            with open(path4, 'w') as k:
                json.dump(data,k)
            #f=open(path3,'w')
            #f.write('DOI_var =' + str(i))
            print(i)
        except ValueError:
            print('Again error')
            Not_find =mapping.GetKey(i)
            h.write(str(i)+': '+Not_find+'\n')

    except IOError as io:
        print('IOError')
        time.sleep(2400)
        os.execl(sys.executable, sys.executable, * sys.argv)
