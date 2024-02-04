from tkinter import *
from tkinter import ttk
from tkinter import messagebox


from Controller.systemLogin import systemLogin

class LoginWindow:

	def __init__(self,conn):
		loginPage = Tk()
		loginPage.configure(bg="#fff")
		loginPage.geometry("700x300")
		loginPage.resizable(False,False)    
		
		def loginn(event):
			systemLogin(conn,entryUsername,entryPassword,loginPage)

		# Input Username
		usernameLabel = Label(text="Masukan Username",bg="#fff")
		usernameLabel.place(x=40,y=10)
		username = StringVar()
		entryUsername = ttk.Entry(text=username)
		entryUsername.place(x=40,y=40)

		# Input Password
		passwordLabel = Label(text="Masukan Password",bg="#fff")
		passwordLabel.place(x=40,y=70)
		password = StringVar()
		entryPassword = ttk.Entry(text=password)
		entryPassword.place(x=40,y=100)
		entryPassword.bind('<Return>',loginn)
		

		# Tombol Login
		checkUser = ttk.Button(text="Login",command=lambda : systemLogin(conn,entryUsername,entryPassword,loginPage))    
		checkUser.place(x=40,y=130)
		
		loginPage.mainloop()

	