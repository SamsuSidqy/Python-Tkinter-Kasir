from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import json
import os


# Controller 
from Controller.db import DatabaseConnect as connectDatabase
from WindowControl.WindowConnect import WindowConnectDatabase as pageWindow



if os.path.isfile('./databaseKasir.json'):
	try:
		read = open("./databaseKasir.json","r")
		jsonDatabase = json.load(read)        
		connectDatabase.withJson(jsonDatabase)
	except Exception as e:
		print(e)
else:
	pageWindow()