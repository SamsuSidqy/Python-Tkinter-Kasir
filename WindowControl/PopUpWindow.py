from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import locale
from datetime import datetime
import json

from WindowControl.LaporanWindow import laporanWindow as lapor


class PopUp:

	def updateBrg(db,idbrg):

		data = {}
		try:
			cur = db.cursor()
			sql = f"SELECT * FROM barang WHERE id_barang={idbrg}"
			cur.execute(sql)
			results = cur.fetchall()
			for r in results:
				data['stok'] = r[4]
				data['namabrg'] = r[2]			
		except Exception as e:
			messagebox.showinfo(message=f"Errors > {e}")
			return False

		def btnmin():			
			data['stok'] -= 1
			if data['stok'] < 0:
				return False
			stok.config(text=data['stok'])

		def btnplus():
			data['stok'] += 1
			stok.config(text=data['stok'])

		def saveData():
			try:
				quer = db.cursor()
				sql=f"UPDATE barang SET stok={stok.cget('text')} WHERE id_barang={idbrg}"
				quer.execute(sql)
				db.commit()
				messagebox.showinfo(message=f"Update Berhasil")
				root.destroy()
			except Exception as e:
				messagebox.showerror(message=f"Err > {e}")
		def hps():
			try:
				query = db.cursor()
				sql = f"DELETE FROM barang WHERE id_barang={idbrg}"
				query.execute(sql)
				db.commit()
				messagebox.showinfo(message=f"Hapus Data Berhasil")
				root.destroy()
			except Exception as e:
				messagebox.showinfo(message=f"Error > {e}")

		root = Tk()
		root.resizable(False,False)
		root.geometry('250x150')
		root.eval('tk::PlaceWindow . center')

		namabrg = Label(root,text=data['namabrg'])
		namabrg.place(relx=0.5,y=25,anchor="center")

		hpusbrg = Button(root,text="Delete",command = lambda: hps())
		hpusbrg.place(x=20,y=15,anchor="center")

		stok = Label(root,text=data['stok'])
		stok.place(relx=0.5,y=65,anchor="center")

		kurang = Button(root,text="-",font=("Arial",20),fg='#fff',bg='black',command= lambda: btnmin())
		kurang.place(x=60,y=65,anchor="center",height=20)

		tambah = Button(root,text="+",font=("Arial",20),fg='#fff',bg='black',command= lambda: btnplus())
		tambah.place(x=195,y=65,anchor="center",height=20)

		tsave = Button(root,text="Save",fg='#fff',bg='black',command= lambda: saveData())
		tsave.place(relx=0.5,y=120,anchor="center",height=20)

		root.mainloop()

	def laporanData(db,mainPage,kasir):
		root = Tk()
		root.resizable(False,False)
		root.geometry('250x150')
		root.eval('tk::PlaceWindow . center')

		def makeLaporan():
			month = klik.get()
			locale.setlocale(locale.LC_TIME,"ID")
			dt = datetime.strptime(month,"%B")
			lp = []
			try:
				query = db.cursor()
				sql = "SELECT * FROM laporan"
				query.execute(sql)
				results = query.fetchall()

				for i in results:
					tgl = i[6]
					datee= datetime.strptime(tgl,"%H:%M:%S | %d, %B, %Y")
					convert = datee.strftime("%B")
					if convert == month:
						lp.append([i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7]])
				income = 0
				sold = 0
				if len(lp) > 0:
					for r in lp:
						income += int(r[3])
						brg = json.loads(r[2]) 
						for i in brg:
							sold += int(i[3])
					data = {
						"totaltrnk":len(lp),
						"income":income,
						"sold":sold,
					}
					lapor.main(mainPage,data,kasir)
					root.destroy()
				else:
					messagebox.showinfo(message=f"Data Bulan {month} Belum Tersedia")
					root.destroy()
			except Exception as e:
				messagebox.showinfo(message=f"{e}")

		option = [
			"Januari",
			"Februari",
			"Maret",
			"April",
			"Mei",
			"Juni",
			"Juli",
			"Agustus",
			"September",
			"Oktober",
			"November",
			"Desember"
		]
		klik = StringVar(root)
		stok = OptionMenu(root,klik,*option)
		stok.place(relx=0.5,y=65,anchor="center")
		
		btnlapor = Button(root,text="Buat Laporan",command= lambda: makeLaporan())
		btnlapor.place(relx=0.5,y=120,anchor="center")

		root.mainloop()










