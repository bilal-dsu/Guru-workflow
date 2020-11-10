# Authors Bilal Hayat Butt, Sufyan Faizi
# Description The code is used to fetch data from the files created from 'JsonDump.py', we extract DOI's from JSON files and populate it in CSV for further analysis.


import json,sys,os

#for getting location of Data Dump
path = os.path.join(os.getcwd(), sys.argv[2], sys.argv[1]+'.csv')
#Making new csv so that we can store our data
DOI_file = open( path, 'w')

newpath = os.path.join(os.getcwd(), sys.argv[2],'Req_count.txt')


with open(newpath, 'r') as f:
	for Value in f:
	
		file_count = int(Value)
		
    	
for Jsonfiles in range(file_count):
	newpathforDataRead = os.path.join(os.getcwd(), sys.argv[2],'Metadata'+str(Jsonfiles)+'_'+sys.argv[2]+'.json')
	with open(newpathforDataRead, 'r') as o:
		Data = json.load(o)
	for records in Data['message']['items']:
		DOI_file.write(records['DOI'] + '\n')
    		 
DOI_file.close()
