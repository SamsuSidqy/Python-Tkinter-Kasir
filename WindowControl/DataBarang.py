import json
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import locale

# Control
from Controller.ShowHidden import ShowHidden
from WindowControl.PopUpWindow import PopUp as popup


listangkaKey = []
class DataBarang:	

	def main(db,kasirFrame,home):
		kasirFrame.place_forget()		
		try:
			cursor = db.cursor()
			sql = "SELECT * FROM barang"
			cursor.execute(sql)
			result = cursor.fetchall()

		except Exception as e:
			messagebox.showinfo(message=f"{e}")

		def keyInput(event):
			global listangkaKey

			equation = ""
			if event.char:
				pass
			equation += event.char
			listangkaKey.append(equation)
			resultKeY = ""
			for i in listangkaKey:
				resultKeY += i
			toIntKey = int(resultKeY)
			locale.setlocale( locale.LC_ALL, 'ID' )
			clientOuputKey =   locale.format("%.0f", toIntKey, grouping=True)
			inputHargaBarang.delete(0, "end")
			inputHargaBarang.insert(0,clientOuputKey)

		def hapus(event):
			global listangkaKey
			listangkaKey.clear()

			inputHargaBarang.delete(0, "end")
			inputHargaBarang.insert(0,"")


		def insertBarang(kode,nama,harga,stok):

			if kode == "" or nama == "" or harga == "" or stok == "":
				messagebox.showinfo(message="Ada Yang Belum Di Isi")
				return False

			try:
				query = db.cursor()
				convertHarga = harga.replace(".","")
				sql = f"INSERT INTO barang VALUES(NULL,'{kode}','{nama}','{convertHarga}',{stok})"
				
				query.execute(sql)
				db.commit()			
				messagebox.showinfo(message="Data Berhasil Ditambahkan")
				inputNamaBarang.delete(0,"end")
				inputKodeBarang.delete(0,"end")
				inputHargaBarang.delete(0,"end")
				inputStokBarang.delete(0,"end")
			except Exception as e:
				messagebox.showerror(message=f"{e}")
		
		def updateBarang(event):
			idbrg = tableBarang.selection()[0]
			popup.updateBrg(db,idbrg)
		

		frameData = Frame(home)
		frameData.place(y=140,x=100,width=1140,height=570)
		tableBarang = ttk.Treeview(frameData)
		tableBarang.place(width=670,height=500)
			

		tableBarang['columns']= ('kode', 'namabrg','hrgabrg','stok')
		tableBarang.column("#0", width=0,  stretch=NO)
		tableBarang.column("kode", anchor=CENTER,width=1 )
		tableBarang.column("namabrg",anchor=CENTER,width=1 )
		tableBarang.column("hrgabrg",anchor=CENTER,width=1 )
		tableBarang.column("stok",anchor=CENTER,width=1)

		tableBarang.heading("kode",text="Kode Barang",anchor=CENTER)
		tableBarang.heading("namabrg",text="Nama Barang",anchor=CENTER)
		tableBarang.heading("hrgabrg",text="Harga Barang",anchor=CENTER)
		tableBarang.heading("stok",text="Stok",anchor=CENTER)

		for row in result:
				locale.setlocale( locale.LC_ALL, 'ID' )
				forharga =   locale.format("%.0f", int(row[3]), grouping=True)
				tableBarang.insert(parent='', index=0, iid=row[0], text='', values=(row[1],row[2],forharga,row[4]))
		tableBarang.bind('<Double-1>',updateBarang)

		scrollbar = ttk.Scrollbar(tableBarang, orient="vertical", command=tableBarang.yview)
		tableBarang.configure(yscroll=scrollbar.set)
		scrollbar.grid(sticky='ns',ipady=225)

		clearTabel = Button(frameData,text="Back Home",command= lambda : ShowHidden.backHome(kasirFrame,frameData))
		clearTabel.place(x=15,y=510,height=40)	

		labelNamabrg = Label(frameData,text="Nama Barang").place(x=680,y=10)
		namabrg = StringVar()
		inputNamaBarang = Entry(frameData,text=namabrg,font=("Arial",25),fg="green")
		inputNamaBarang.place(x=680,y=40,width=420)

		labelKodebrg = Label(frameData,text="Kode Barang").place(x=680,y=90)
		kodebrg = StringVar()
		inputKodeBarang = Entry(frameData,text=kodebrg,font=("Arial",25),fg="green")
		inputKodeBarang.place(x=680,y=120,width=420)

		labelsHargabrg = Label(frameData,text="Harga Barang").place(x=680,y=170)
		hargabrg = StringVar()
		inputHargaBarang = Entry(frameData,text=hargabrg,font=("Arial",25),fg="green")
		inputHargaBarang.bind('<KeyRelease>',keyInput)		
		inputHargaBarang.bind("<BackSpace>",hapus)
		inputHargaBarang.place(x=680,y=200,width=420)

		labelsStokbrg = Label(frameData,text="Stok Barang").place(x=680,y=250)
		stokbr = IntVar()
		inputStokBarang = Entry(frameData,text=stokbr,font=("Arial",25),fg="green")
		inputStokBarang.place(x=680,y=280,width=420)

		buttonData = Button(frameData,text=" Tambah Data", bg="grey",font=("Arial",10,"bold"),width=90,
			command= lambda : insertBarang(inputKodeBarang.get(),inputNamaBarang.get(),inputHargaBarang.get(),inputStokBarang.get()))
		buttonData.place(x=700,y=350,width=400)