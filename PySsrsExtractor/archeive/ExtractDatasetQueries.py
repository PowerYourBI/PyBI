

import pandas as pd
import xml.etree.ElementTree as ET
import io
import os


sep = f"+++++++++++++++++++++++++++++++++++++++++++++"

directory = r'C:\Users\Jaouad\Documents\Python Practice\ssrsexctract/'
query = r'C:\Users\Jaouad\Documents\Python Practice\ssrsexctract\Query/'

for file in os.listdir(directory):
	filename = os.fsdecode(file)
	if filename.endswith(".rdl"):
		# print(os.path.join(directory, filename))
		xml_data = os.path.join(directory, filename)
		ReportName = filename.split('.')[0] 
		file = open(f'{query}{ReportName}.txt' ,"w") 

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
					print(Sep + '\n' +querytext.text + '\n')
					file.write(Sep + '\n' +querytext.text + '\n')
		file.close()

