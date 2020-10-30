import json,os,sys

path = os.path.join(os.getcwd(), sys.argv[2], sys.argv[1]+'.csv')


doi_author_file = open(path , 'w',encoding='utf-8')

path = os.path.join(os.getcwd(), sys.argv[2],'Req_count.txt')
with open(path, 'r') as Req_count_file:
	for Value in Req_count_file:
    	  file_count = int(Value)
    
for Jsonfiles in range(file_count):
    newpathforDataRead = os.path.join(os.getcwd(), sys.argv[2],'Metadata'+str(Jsonfiles)+'_'+sys.argv[2]+'.json')
    with open(newpathforDataRead , 'r') as JsonData:
   		 Data = json.load(JsonData)

    for records in Data['message']['items']:
   	 Author_Name = ''
   	 try:
   		 for Author in records['author']:
   			 Author_Name = Author_Name + ',' + Author['given'] + ' ' + Author['family']
   		 
   		 doi_author_file.write(records['DOI'] +  str(Author_Name) + '\n') 
   	 except KeyError:
   		 pass
doi_author_file.close()
path = os.path.join(os.getcwd(), sys.argv[2], sys.argv[1]+'.csv')
fread = open(path , 'r',encoding='utf-8')
data = fread.read()
#data = data.replace(' ' , '_')
fread.close()
fwrite = open(path , 'w',errors='ignore')
fwrite.write(data)
fwrite.close()