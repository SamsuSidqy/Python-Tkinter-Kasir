import json
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import locale
import random
import string




class Transaksi:


	def main(db,kasirFrame,home,data):
		kasirFrame.place_forget()

		frameData = Frame(home)
		frameData.place(y=140,x=100,width=1140,height=570)
		dump = json.loads(data)
		
		locale.setlocale( locale.LC_ALL, 'ID' )
		tunai =  locale.format("%.0f", int(dump['jumlahbayar']), grouping=True)
		total =  locale.format("%.0f", int(dump['totalbayar']), grouping=True)
		kembali =  locale.format("%.0f", int(dump['kembalian']), grouping=True)		


		# Ini Untuk Token Verify
		acak2 = "[a-z,A-Z,`~!@$]"
		def generate_random_token(length):
		    token = ''.join(random.choice(acak2 + string.ascii_letters + string.digits) for _ in range(length))
		    return token

		def cancel():
			frameData.place_forget()
			kasirFrame.place(y=140,x=100,width=1140,height=570)

		def saveTransaksi():
			query = db.cursor()
			dump = json.loads(data)
			dataArray = json.dumps(dump['table'])
			kode = generate_random_token(30)
			sql = f"INSERT INTO laporan VALUES (NULL,'TRNK-{kode}','{dataArray}','{dump['totalbayar']}','{dump['jumlahbayar']}','{dump['kembalian']}','{dump['date']}','{dump['metode']}')"	
			try:
				for i in dump['table']:
					cek = query.execute(f"SELECT * FROM barang WHERE kode_barang='{i[0]}'")
					result = query.fetchall()
					if len(result) > 0:
						for r in result:
							if int(r[4]) == 0:
								messagebox.showinfo(message="Stok Barang Lagi Kosong")
								return False
							updateStok = int(r[4]) - int(i[3])
							if updateStok < 0:
								messagebox.showinfo(message="Stok Barang Tidak Mencukupi")
								return False
							query.execute(f"UPDATE barang SET stok={updateStok} WHERE kode_barang='{r[1]}'")
							db.commit()					
					else:
						messagebox.showinfo(message="Barang Tidak Di Temukan")
						return False
				query.execute(sql)
				db.commit()
				messagebox.showinfo(message="Data Berhasil Di Save")
			except Exception as e:
				messagebox.showinfo(message=f"Error = {e}")
		

		labelTotalBelanaja = Label(frameData,text="Total Belanjaan ",font=("Arial",20,"bold"))
		labelTotalBelanaja.place(x=700)
		showTotalBelanja = Label(frameData,text="100,000,000",bg="black",font=("Arial",20),fg="green")
		showTotalBelanja.place(x=940,width=200) 

		labelTotalTunai = Label(frameData,text="Total Uang  ",font=("Arial",20,"bold"))
		labelTotalTunai.place(x=700,y=55)
		showTotalTunai = Label(frameData,text="100,000,000",bg="black",font=("Arial",20),fg="green")
		showTotalTunai.place(x=940,y=55,width=200) 

		labelTotalKembalian = Label(frameData,text="Kembalian ",font=("Arial",20,"bold"))
		labelTotalKembalian.place(x=700,y=115)
		showTotalKembalian = Label(frameData,text="20.000",bg="black",font=("Arial",20),fg="green")
		showTotalKembalian.place(x=940,y=115,width=200) 

		showTotalTunai.config(text=tunai)
		showTotalKembalian.config(text=kembali)
		showTotalBelanja.config(text=total)

		buttonSave = Button(frameData,text="Save",command= lambda : saveTransaksi())
		buttonSave.place(x=700,y=200,width=120)

		buttonPrint = Button(frameData,text="Print Struck")
		buttonPrint.place(x=830,y=200,width=120)

		buttonCancel = Button(frameData,text="Cancel",command= lambda : cancel())
		buttonCancel.place(x=960,y=200,width=120)

		sett = ttk.Treeview(frameData)
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

		for row in dump['table']:
			sett.insert(parent='', index=0, iid=row[0], text='', values=(row[0], row[1], row[2], row[3]))

		scrollbar = ttk.Scrollbar(sett, orient="vertical", command=sett.yview)
		sett.configure(yscroll=scrollbar.set)
		scrollbar.grid(sticky='ns',ipady=225)

