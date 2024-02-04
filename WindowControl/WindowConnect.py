from tkinter import *
from tkinter import ttk
from tkinter import messagebox


# Controller
from Controller.db import DatabaseConnect as connectDatabase


class WindowConnectDatabase:

	def __init__(self):
		window = Tk()

		window.configure(bg="#fff")
		window.geometry("200x300")
		window.resizable(False,False)

		database = Label(text = 'Nama Database', font=('calibre',10, 'bold'),bg="#fff")
		database.place(x=10,y=10)

		database = StringVar()
		entryDatabse = ttk.Entry(text=database)
		entryDatabse.place(x=10,y=40)

		passwordDatabase = Label(text = 'Password Database', font=('calibre',10, 'bold'),bg="#fff")
		passwordDatabase.place(x=10,y=70)

		passwordDatabase = StringVar()
		entryPassword = ttk.Entry(text=passwordDatabase)
		entryPassword.place(x=10,y=100)

		user = Label(text = 'User Database', font=('calibre',10, 'bold'),bg="#fff")
		user.place(x=10,y=130)

		user = StringVar()
		userDatabse = ttk.Entry(text=user)
		userDatabse.place(x=10,y=160)

		checkDatabase = ttk.Button(text="Connect Database",
			command=lambda : connectDatabase.withoutJson(window,userDatabse.get(),entryPassword.get(),entryDatabse.get()))
		checkDatabase.place(x=10,y=230)

		window.mainloop()
