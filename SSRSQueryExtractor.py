from numpy.lib.function_base import disp
import pandas as pd
import requests
from requests_ntlm import HttpNtlmAuth
from requests import Session
import json
import xml.etree.ElementTree as ET
import io
import os
import tkinter as tk
from tkinter import Canvas, Image
from tkinter import font
session = Session()
root = tk.Tk()
HIEGHT =500
WIDTH = 700




def Start_Extraction(username, password, server):

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
			# print(f' {name} Report was downloaded')

	sep = f"--+++++++++++++++++++++++++++++++++++++++++++++"

	directory = 'C:\\Users\\'+username+'\\Documents\\Python Practice\\PySsrsExtractor\\ssrsexctract//'
	query = 'C:\\Users\\'+username+'\\Documents\\Python Practice\\PySsrsExtractor\\ssrsexctract\\Query//'

	if not os.path.exists('directory'):
		os.makedirs('directory')
		print('Created Directory' + directory)

	if not os.path.exists('query'):
		os.makedirs('query')
		print('Created Directory' + query)

	Reportpath =[]
	for file in os.listdir(directory):
		filename = os.fsdecode(file)
		if filename.endswith(".rdl"):
			# print(os.path.join(directory, filename))
			xml_data = os.path.join(directory, filename)
			ReportName = filename.split('.')[0] 
			file = open(f'{query}{ReportName}.sql' ,"w") 

			xml_data = os.path.join(directory, filename)
			# print(xml_data)
			Reportpath.append(filename)
			tree = ET.parse(xml_data)
			root = tree.getroot()
			
			for ds in root.findall('{http://schemas.microsoft.com/sqlserver/reporting/2016/01/reportdefinition}DataSets'):
				d = ds.findall('{http://schemas.microsoft.com/sqlserver/reporting/2016/01/reportdefinition}DataSet')
				for q in d:
					r = q.find('{http://schemas.microsoft.com/sqlserver/reporting/2016/01/reportdefinition}Query')
					labelList=[]
					for querytext in r.findall('{http://schemas.microsoft.com/sqlserver/reporting/2016/01/reportdefinition}CommandText'):
						Sep = '{}-- {} --{} '.format( sep , filename ,sep)
						# print(Sep + '\n' +querytext.text + '\n')
						
						file.write(Sep + '\n' +querytext.text + '\n')
			file.close()
	# print()
	# print('Finished Extracting Queries Successfully!')
	Display=  pd.DataFrame(Reportpath)
	Columns = ['Reports']
	Display.columns=Columns
	label['text']= Display


canvas = tk.Canvas(root, height= HIEGHT , width = WIDTH)
canvas.pack()


frame = tk.Frame(root, bg ='#80c1ff', bd=5)
frame.place(relx = 0.5, rely= 0.1, relwidth =1, relheight=0.3, anchor='n')

entryuser = tk.Entry(frame, font=20)
entryuser.place(relx=0.25, rely =0.1, relwidth =0.4, relheight=0.20)
entrypass = tk.Entry(frame,  font=30)
entrypass.place(relx=0.25, rely =0.4,relwidth =0.4, relheight=0.20)
entryserver = tk.Entry(frame, font=20)
entryserver.place(relx=0.25, rely =0.70,relwidth =0.4, relheight=0.20)

label = tk.Label(frame, font = ('Segoue',16),text='Username: ', bg ='#80c1ff', anchor='nw', justify='left', bd =4)
label.place( relx=0, rely =0.1, relwidth =0.2, relheight=1)

label = tk.Label(frame, font = ('Segoue',16), text='Password: ', bg ='#80c1ff', anchor='nw', justify='left', bd =4)
label.place( relx=0, rely =0.4, relwidth =0.2, relheight=1)

label = tk.Label(frame, font = ('Segoue',16),text='Servername: ',bg ='#80c1ff', anchor='nw', justify='left', bd =4)
label.place( relx=0, rely =0.70, relwidth =0.2, relheight=1)


button = tk.Button(frame, text='Start Extraction', font =30, command=lambda: Start_Extraction(entryuser.get(),entrypass.get(), entryserver.get() ))
button.place(relx=0.70, relheight=0.4, relwidth =0.3 )

lower_frame= tk.Frame(root, bg ='#80c1ff', bd = 10)
lower_frame.place(relx=0.5, rely=0.45, relwidth=1, relheight=0.5, anchor='n')

label = tk.Label(lower_frame, font = ('Segoue',18),anchor='nw', justify='left', bd =4)
label.place( relwidth =1, relheight=1)
root.mainloop()
