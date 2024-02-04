import json
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from time import strftime
import locale


# Control
from WindowControl.KasirWindow import KasirMain 

class systemLogin:

	def __init__(self,db,username,password,loginPage):
		user = username.get()
		pswd = password.get()

		cursor = db.cursor()
		sql = f"SELECT * FROM users WHERE username='{user}' AND password='{pswd}'"
		cursor.execute(sql)
		result = cursor.fetchall()
		cursor.close()
		if len(result) == 0:
			messagebox.showinfo(message=f'Password Or Username Is Wrong')
			return False		
		messagebox.showinfo(message=f'Success Login, Selamat Berkerja')
		loginPage.destroy()
		KasirMain.showKasir(db)
