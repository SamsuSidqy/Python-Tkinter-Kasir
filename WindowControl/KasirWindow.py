import json
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from time import strftime
import locale

# Control
from WindowControl.DataBarang import DataBarang as databarang
from WindowControl.TransaksiWindow import Transaksi 
from WindowControl.PopUpWindow import PopUp as popup


listangka = []
listangkaKey = []
totalHarga = []
listKerjanjang = []
keyKeranjang = ""


class KasirMain:	

	def showKasir(db):		

		mainPage = Tk()
		mainPage.state('zoomed')
		mainPage.configure(bg="Blue")
		mainPage.resizable(False,False)	
		mainPage.title("Tes Gui")

		def on_entry_click(event):
			if inputBarang.get() == "Kode / Nama Barang":
				inputBarang.delete(0, "end")  # delete all the text in the entry
				inputBarang.insert(0, "")

		def on_focus_out(event):
			if inputBarang.get() == "":
				inputBarang.insert(0, "Kode / Nama Barang")
				inputBarang.config(fg='grey')  # set text color to grey



		
		def showing(value):
			global listangka
			equation =""
			equation += value
			listangka.append(equation)
			result = ""
			for i in listangka:
				result += i
			toInt = int(result)
			locale.setlocale( locale.LC_ALL, 'ID' )
			clientOuput =  locale.format("%.0f", toInt, grouping=True)
			inputBayar.delete(0, "end")
			inputBayar.insert(0,clientOuput)

		
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
			inputBayar.delete(0, "end")
			inputBayar.insert(0,clientOuputKey)


		def hapus(event=None):
			global listangka
			global listangkaKey
			listangka.clear()
			listangkaKey.clear()
			inputBayar.delete(0, "end")

		

		def searchBrg():
				brgKode = inputBarang.get()
				query = db.cursor()
				sql = f"SELECT * FROM barang WHERE kode_barang='{brgKode}'"
				try:			
					query.execute(sql)
					results = query.fetchall()
					list1 = None
					global totalHarga
					global listKerjanjang
					global keyKeranjang
					for x in results:
						locale.setlocale( locale.LC_ALL, 'ID' )
						formatrp =  locale.format("%.0f", int(x[3]), grouping=True)
						harga = x[3]
						quanty = 0
						list1 = [x[1], x[2], formatrp]
						keyKeranjang += list1[0]								
					if len(results) > 0 :
						totalHarga.append(harga)
						listKerjanjang.append(list1)
						# print(listKerjanjang)								
						totl = 0
						for x in totalHarga:
							totl += int(x)	
						for r in listKerjanjang:					
							if brgKode in r:
								quanty += 1
								finalist = [r[0],r[1],r[2],quanty]
							else:
								finalist = None

						if finalist is not None:
							try:
								item_exists = sett.exists(finalist[0])

								if item_exists:
									# Update the values for the existing item
									sett.item(finalist[0], values=(finalist[0], finalist[1], finalist[2], finalist[3]))
								else:
									# Insert a new item if it doesn't exist
									sett.insert(parent='', index=0, iid=finalist[0], text='', values=(finalist[0], finalist[1], finalist[2], finalist[3]))
							except Exception as e:
								print(e)

						totalFormat = locale.format("%.0f", totl, grouping=True)				
						showTotal.config(text=totalFormat)
					else:
						messagebox.showinfo(message=f'Barang Tidak Di Temukan')
					query.close()
				except Exception as e:
					messagebox.showinfo(message=f'{e}')
					query.close()
				inputBarang.delete(0,"end")


		def clearTabelBrg():
			global totalHarga
			global listKerjanjang
			global listangka
			global listangkaKey
			listangka.clear()
			listangkaKey.clear()
			totalHarga.clear()
			listKerjanjang.clear()
			for i in sett.get_children():
				sett.delete(i)
			showTotal.configure(text="0")
			inputBayar.delete(0,"end")
			inputBayar.insert(0,"")

		def transaksi():
			global listangkaKey
			data = []
			for i in sett.get_children():
				data.append(sett.item(i)['values'])
			jmlhbyr = inputBayar.get().replace(".","")
			total = showTotal.cget("text").replace(".","")
			if int(jmlhbyr) < int(total):
				messagebox.showinfo(message="Pembayaran Tidak Mencukupi")
				return False
			elif len(data) < 0:
				messagebox.showinfo(message="Tabel Belanja Masih Kosong")
				return False
			elif jmlhbyr is None:
				messagebox.showinfo(message="Masukan Jumlah Pembayaran")
				return False

			kembalian = int(jmlhbyr) - int(total)
			locale.setlocale(locale.LC_TIME,"id-ID")
			dataJson = {
				"table":data,
				"metode":metode.get(),
				"jumlahbayar":jmlhbyr,
				"totalbayar":total,
				"kembalian":kembalian,
				"date":strftime('%H:%M:%S | %d, %B, %Y')
			}
			jsons = json.dumps(dataJson)
			Transaksi.main(db,kasirFrame,mainPage,jsons)



		

		
		kasirFrame = Frame(mainPage,bg="lightblue")
		sett = ttk.Treeview(kasirFrame)
		sett.place(width=670,height=500)
			

		sett['columns']= ('kode', 'namabrg','hrgabrg','jmlh')
		sett.column("#0", width=0,  stretch=NO)
		sett.column("kode", anchor=CENTER,width=1 )
		sett.column("namabrg",anchor=CENTER,width=1 )
		sett.column("hrgabrg",anchor=CENTER,width=1 )
		sett.column("jmlh",anchor=CENTER,width=1)

		sett.heading("kode",text="Kode Barang",anchor=CENTER)
		sett.heading("namabrg",text="Nama Barang",anchor=CENTER)
		sett.heading("hrgabrg",text="Harga Barang",anchor=CENTER)
		sett.heading("jmlh",text="Jumlah",anchor=CENTER)

		scrollbar = ttk.Scrollbar(sett, orient="vertical", command=sett.yview)
		sett.configure(yscroll=scrollbar.set)
		scrollbar.grid(sticky='ns',ipady=225)

		clearTabel = Button(kasirFrame,text="Clear Keranjang",
			command= lambda : clearTabelBrg())
		clearTabel.place(x=15,y=510,height=40)

		



		showTotal = Label(kasirFrame,text="0",bg="black",font=("Arial",30),fg="green")
		showTotal.place(x=670,width=470)

		brgInput = StringVar()
		inputBarang = Entry(kasirFrame,text=brgInput,font=("Arial",25),fg="green")
		inputBarang.insert(0, "Kode / Nama Barang")
		inputBarang.bind('<FocusIn>', on_entry_click)
		inputBarang.bind('<FocusOut>', on_focus_out)
		inputBarang.place(x=670,y=55,width=320)

		EnterBrgInput = Button(kasirFrame,text="Enter",bg="green",fg="#fff",font=("Arial",15),
			command= lambda : searchBrg())
		EnterBrgInput.place(x=997,y=55,height=45,width=130)
		kasirFrame.place(y=140,x=100,width=1140,height=570)

		choices = ['CASH', 'BANK']
		variable = StringVar()
		variable.set(choices[0])

		metode = StringVar()
		metode.set(None)
		metodePembayaranBank = Radiobutton(kasirFrame, variable=metode, text="BANK", value="BANK",font=("Arial",20,"bold"))
		metodePembayaranBank.place(y=105,x=850)
		metodePembayaranTunai = Radiobutton(kasirFrame,variable=metode, text="TUNAI", value="TUNAI",font=("Arial",20,"bold"))
		metodePembayaranTunai.place(y=105,x=680)

		jumlahBayar = StringVar()
		inputBayar = Entry(kasirFrame,text=jumlahBayar,font=("Arial",25))
		inputBayar.bind('<KeyRelease>',keyInput)
		inputBayar.bind("<BackSpace>",hapus)
		inputBayar.place(x=670,y=170,width=320)
		EnterInputBayar = Button(kasirFrame,command=lambda : transaksi(),text="Enter",bg="green",fg="#fff",font=("Arial",15))
		EnterInputBayar.place(x=997,y=170,height=45,width=130)

		# Tombol Angka


		number1 = Button(kasirFrame,text="1",bg="black",fg="#fff",font=("Arial",15),command= lambda : showing("1"))
		number1.place(x=670,y=230,height=45,width=80)
		number2 = Button(kasirFrame,text="2",bg="black",fg="#fff",font=("Arial",15),command= lambda : showing("2"))
		number2.place(x=760,y=230,height=45,width=80)
		number3 = Button(kasirFrame,text="3",bg="black",fg="#fff",font=("Arial",15),command= lambda : showing("3"))
		number3.place(x=850,y=230,height=45,width=80)
		number4 = Button(kasirFrame,text="4",bg="black",fg="#fff",font=("Arial",15),command= lambda : showing("4"))
		number4.place(x=940,y=230,height=45,width=80)
		number5 = Button(kasirFrame,text="5",bg="black",fg="#fff",font=("Arial",15),command= lambda : showing("5"))
		number5.place(x=1030,y=230,height=45,width=80)

		number6 = Button(kasirFrame,text="6",bg="black",fg="#fff",font=("Arial",15),command= lambda : showing("6"))
		number6.place(x=670,y=280,height=45,width=80)
		number7 = Button(kasirFrame,text="7",bg="black",fg="#fff",font=("Arial",15),command= lambda : showing("7"))
		number7.place(x=760,y=280,height=45,width=80)
		number8 = Button(kasirFrame,text="8",bg="black",fg="#fff",font=("Arial",15),command= lambda : showing("8"))
		number8.place(x=850,y=280,height=45,width=80)
		number9 = Button(kasirFrame,text="9",bg="black",fg="#fff",font=("Arial",15),command= lambda : showing("9"))
		number9.place(x=940,y=280,height=45,width=80)
		number0 = Button(kasirFrame,text="0",bg="black",fg="#fff",font=("Arial",15),command= lambda : showing("0"))
		number0.place(x=1030,y=280,height=45,width=80)

		rp100rb = Button(kasirFrame,text="100 Rb",bg="black",fg="#fff",font=("Arial",15),command= lambda : showing("100000"))
		rp100rb.place(x=670,y=330,height=45,width=80)
		rp50rb = Button(kasirFrame,text="50 Rb",bg="black",fg="#fff",font=("Arial",15),command= lambda : showing("50000"))
		rp50rb.place(x=760,y=330,height=45,width=80)
		rp20rb = Button(kasirFrame,text="20 Rb",bg="black",fg="#fff",font=("Arial",15),command= lambda : showing("20000"))
		rp20rb.place(x=850,y=330,height=45,width=80)
		rp10rb = Button(kasirFrame,text="10 Rb",bg="black",fg="#fff",font=("Arial",15),command= lambda : showing("10000"))
		rp10rb.place(x=940,y=330,height=45,width=80)
		delet = Button(kasirFrame,text="C",bg="black",fg="#fff",font=("Arial",15),command= lambda : hapus())
		delet.place(x=1030,y=330,height=45,width=80)


		# Jam
		def waktuJam():
			locale.setlocale(locale.LC_TIME,"id-ID")
			string = strftime('%H:%M:%S | %d, %B, %Y')
			jam.config(text=string)
			jam.after(1000, waktuJam)

		jam = Label(kasirFrame,font=("Arial",20,"bold"),bg="pink")
		jam.place(width=400,x=700,y=525)
		waktuJam()


		# Logo Home
		homeImage=Image.open('../Asset/home.png')
		homeImage = homeImage.resize((40,40))
		imageHome=ImageTk.PhotoImage(homeImage)
		# Logo Kasir
		kasirImage=Image.open('../Asset/kasir.png')
		kasirImage = kasirImage.resize((40,40))
		imageKasir=ImageTk.PhotoImage(kasirImage)
		# Logo Laporan
		reportImage=Image.open('../Asset/laporan.png')
		reportImage = reportImage.resize((40,40))
		imageReport=ImageTk.PhotoImage(reportImage)
		# Logo Data
		dataImage=Image.open('../Asset/data.png')
		dataImage = dataImage.resize((40,40))
		imageData=ImageTk.PhotoImage(dataImage)


		buttonLaporan = Button(kasirFrame,text=" Laporan",bg="grey",font=("Arial",10,"bold"),command= lambda : popup.laporanData(db,mainPage,kasirFrame) ,height=40,width=90,image = imageReport,compound ="left")
		buttonLaporan.place(x=700,y=400,width=400)

		buttonData = Button(kasirFrame,text=" Data Barang", bg="grey",font=("Arial",10,"bold"),command= lambda : databarang.main(db,kasirFrame,mainPage),height=40,width=90,image = imageData,compound ="left")
		buttonData.place(x=700,y=455,width=400)		


		mainPage.mainloop()