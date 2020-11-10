"""
Created on Sun Nov 24 2019
@author: Bilal Hayat Butt, Sufyan Faizi
@Description: The code makes API call to crossref with given ISSN, start date and end date which returns JSON response, the response used to create data dump of crossref 

"""


import sys,os
import json, requests #pip install requests

#Variable initialization
Start_Date , End_Date = sys.argv[1] , sys.argv[2]
ISSN , offset = sys.argv[3] , 0

#getting current directory and dumping data in that directory
path = os.path.join(os.getcwd(), sys.argv[4])

if not os.path.exists(path): #check if folder already exist, if it doesn't then create it
    os.makedirs(path)

#Crossref API Call
API_String = 'http://api.crossref.org/works?filter=issn:'+ISSN+',from-pub-date:'+Start_Date+',until-pub-date:'+End_Date+'&rows=1000'
response = requests.get(API_String)
data = response.json()

# No of Records in Journal
Records = data['message']['total-results']
Req_count = Records / 1000
Rem = Records % 1000
    
if Rem == 0:
    Req_count = int(Req_count)
else:
    Req_count = int(Req_count) + 1

newpath = os.path.join(os.getcwd(), sys.argv[4],'Req_count.txt')
Request_Count_file = open(newpath , 'w')
Request_Count_file.write(str(Req_count))    
Request_Count_file.close()


# Save data in Json files
for Request in range(int(Req_count)):
		response = requests.get(API_String+'&offset='+str(offset))
		data = response.json()
		newpathforDataDump = os.path.join(os.getcwd(), sys.argv[4],'Metadata'+str(Request)+'_'+sys.argv[4]+'.json')
		with open(newpathforDataDump, 'w') as f1:
				json.dump(data , f1)
				offset = offset + 1000
