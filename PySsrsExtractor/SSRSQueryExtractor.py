
import requests
from requests_ntlm import HttpNtlmAuth
from requests import Session
import json
import xml.etree.ElementTree as ET
import io
import os

session = Session()

# username = r'jmac\Jaouad'
# password = '1956'

user = input('Enter your username: ')
pwd = input('Enter you password: ')
serv = input('Enter Server name: ')

username = str(user)
password = str(pwd)
server = str(serv)

url = "http://"+server+"/reports/api/v2.0/reports"

r = requests.get(url, auth=HttpNtlmAuth(username, password))
response = session.get(url)
#print(r.status_code)
rr = r.json()
# rr_str = json.dumps(rr, indent=2)
# print(rr_str)

d=[]
for value in rr['value']:
    data =[ value['Name'], value['Id'] ]
    d.append(data)

for name, ReportID in d:
    uri ="http://"+server+"/Reports/api/v2.0/DataSets(" +ReportID + ")/Content/$value"
   
    rs = requests.get(uri, auth=HttpNtlmAuth(username, password))
    response = session.get(uri)

    with open('ssrsexctract\\'+name+'.rdl', 'wb') as file:
        file.write(rs.content)
        print(f' {name} Report was downloaded')

sep = f"--+++++++++++++++++++++++++++++++++++++++++++++"

directory = 'C:\\Users\\'+username+'\\Documents\\Python Practice\\PySsrsExtractor\\ssrsexctract//'
query = 'C:\\Users\\'+username+'\\Documents\\Python Practice\\PySsrsExtractor\\ssrsexctract\\Query//'

if not os.path.exists('directory'):
    os.makedirs('directory')
    print('Created Directory' + directory)

if not os.path.exists('query'):
    os.makedirs('query')
    print('Created Directory' + query)


for file in os.listdir(directory):
	filename = os.fsdecode(file)
	if filename.endswith(".rdl"):
		# print(os.path.join(directory, filename))
		xml_data = os.path.join(directory, filename)
		ReportName = filename.split('.')[0] 
		file = open(f'{query}{ReportName}.sql' ,"w") 

		xml_data = os.path.join(directory, filename)
		print(xml_data)
		tree = ET.parse(xml_data)
		root = tree.getroot()
		
		for ds in root.findall('{http://schemas.microsoft.com/sqlserver/reporting/2016/01/reportdefinition}DataSets'):
			d = ds.findall('{http://schemas.microsoft.com/sqlserver/reporting/2016/01/reportdefinition}DataSet')
			for q in d:
				r = q.find('{http://schemas.microsoft.com/sqlserver/reporting/2016/01/reportdefinition}Query')
				for querytext in r.findall('{http://schemas.microsoft.com/sqlserver/reporting/2016/01/reportdefinition}CommandText'):
					Sep = '{}-- {} --{} '.format( sep , filename ,sep)
					# print(Sep + '\n' +querytext.text + '\n')
					print('Query for {} was extracted'.format(filename))
					
					file.write(Sep + '\n' +querytext.text + '\n')
		file.close()
print()
print('Finished Extracting Queries Successfully!')