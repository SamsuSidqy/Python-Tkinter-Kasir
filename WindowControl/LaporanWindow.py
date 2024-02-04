from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import locale
import os



class laporanWindow:

	def main(root,data,kasir):
		kasir.place_forget()
		frameLapor = Frame(root)
		frameLapor.place(y=140,x=100,width=1140,height=570)	


		def backHome():
			frameLapor.place_forget()	
			kasir.place(y=140,x=100,width=1140,height=570)	

		inc = data['income']
		locale.setlocale( locale.LC_ALL, 'ID' )
		formatrp =  locale.format("%.0f", inc, grouping=True)

		btntnk = Button(frameLapor,text=f"Transaction ({data['totaltrnk']})",bg="black",fg="#fff",font=("Arial",13,"bold"))
		btntnk.place(x=100,y=50,width=200,height=100)

		btnsold = Button(frameLapor,text=f"Sold ({data['sold']})",bg="black",fg="#fff",font=("Arial",13,"bold"))
		btnsold.place(x=350,y=50,width=200,height=100)

		bntrp = Button(frameLapor,text=f"Rp. {formatrp}",bg="black",fg="green",font=("Arial",13,"bold"))
		bntrp.place(x=600,y=50,width=200,height=100)

		btnrlos = Button(frameLapor,text=f" 0% ",bg="black",fg="red",font=("Arial",13,"bold"))
		btnrlos.place(x=850,y=50,width=200,height=100)

		btnBack = Button(frameLapor,text=f"Back Home",font=("Arial",13,"bold"),command = lambda : backHome())
		btnBack.place(x=100,y=500,width=150,height=50)

		
