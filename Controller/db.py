import mysql.connector as sql 
from mysql.connector import errorcode
import json
import os
from tkinter import messagebox

# Controller
from WindowControl.LoginWindow import LoginWindow as login


class DatabaseConnect:


	def withJson(data=None):
			
		userDatabase = data['username']
		passwordDatabase = None
		databaseName = data['database']

		if data['password']:
			passwordDatabase = ''
		else:
			passwordDatabase = data['password']

		try:
			conn = sql.connect(user=userDatabase,password=passwordDatabase,host='localhost',database=databaseName)
			messagebox.showinfo(message="Connected Success")
			login(conn)
		except sql.Error as err:
			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				messagebox.showerror(message="Username Or Password Wrong")
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				messagebox.showerror(message="Database Does Not Exist")
			else:
				messagebox.showerror(message=f"{err}")
	
	def withoutJson(page,username,password,database):
		page.destroy()
		userDatabase = username
		passwordDatabase = None
		databaseName = database
		if password:
			passwordDatabase = ''
		else:
			passwordDatabase = password
		try:
			conn = sql.connect(user=userDatabase,password=passwordDatabase,host='localhost',database=databaseName)
			messagebox.showinfo(message="Connected Success")
			dataJson = {
				"database":database,
				"username":username,
				"password":password
			}
			objk = json.dumps(dataJson,indent=3)
			cretateJsonDatabase = open("databaseKasir.json","w")
			cretateJsonDatabase.write(objk)
			login(conn)
		except sql.Error as err:
			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				messagebox.showerror(message="Username Or Password Wrong")
			elif err.errno == ER_BAD_DB_ERROR:
				messagebox.showerror(message="Database Does Not Exist")
			else:
				messagebox.showerror(message=f"{err}")
	





	


