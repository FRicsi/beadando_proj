from tkinter import *
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime

class Szoba:
    def __init__(self, szobsz, ar):
        self.szobsz = szobsz
        self.ar = ar

class EgyagyasSzoba(Szoba):
    def __init__(self, szobsz):
        super().__init__(szobsz, 5000)

class KetagyasSzoba(Szoba):
    def __init__(self, szobsz):
        super().__init__(szobsz, 8000)

class Foglalas:
    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum

class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.fgl_ok = []

    def add_szoba(self, szoba):
        self.szobak.append(szoba)

    def fgls(self, szobsz, datum):
        for szoba in self.szobak:
            if szoba.szobsz == szobsz:
                fgls = fgls(szoba, datum)
                self.fgl_ok.append(fgls)
                return szoba.ar
        return None

    def lemond(self, szobsz, datum):
        for fgls in self.fgl_ok:
            if fgls.szoba.szobsz == szobsz and fgls.datum == datum:
                self.fgl_ok.remove(fgls)
                return True
        return False

    def listaz_fgl_ok(self):
        fgl_ok_str = ""
        for fgls in self.fgl_ok:
            fgl_ok_str += f"Szoba: {fgls.szoba.szobsz}, Dátum: {fgls.datum}\n"
        return fgl_ok_str

def fgls_gomb_click():
    szobsz = szobsz_entry.get()
    datum = datum_cal.selection_get()
    if datum:
        ar = hotel.fgls(szobsz, datum)
        if ar:
            messagebox.showinfo("Sikeres foglalás", f"A foglalás sikeres! Az ár: {ar} Ft")
        else:
            messagebox.showerror("Hiba", "Hibás szobaszám!")
    else:
        messagebox.showerror("Hiba", "Válassz egy dátumot!")

def lemond_gomb_click():
    szobsz = szobsz_lemond_entry.get()
    datum = datum_lemond_cal.selection_get()
    if datum:
        sikeres = hotel.lemond(szobsz, datum)
        if sikeres:
            messagebox.showinfo("Sikeres lemondás", "A foglalás sikeresen lemondva.")
        else:
            messagebox.showerror("Hiba", "Nincs ilyen foglalás.")
    else:
        messagebox.showerror("Hiba", "Válassz egy dátumot!")

def listaz_gomb_click():
    fgl_ok = hotel.listaz_fgl_ok()
    if fgl_ok:
        messagebox.showinfo("Foglalások listája", fgl_ok)
    else:
        messagebox.showinfo("Foglalások listája", "Nincs foglalás")

# Szalloda létrehozása
hotel = Szalloda("Pihenő Hotel")
hotel.add_szoba(EgyagyasSzoba("101"))
hotel.add_szoba(EgyagyasSzoba("102"))
hotel.add_szoba(KetagyasSzoba("201"))

# Tkinter ablak létrehozása
ablak = Tk()
ablak.title("Szobafoglalás")

# Foglalás rész
fgls_frame = LabelFrame(ablak, text="Foglalás")
fgls_frame.grid(row=0, column=0, padx=10, pady=10)

Label(fgls_frame, text="Szobaszám:").grid(row=0, column=0)
szobsz_entry = Entry(fgls_frame)
szobsz_entry.grid(row=0, column=1)

Label(fgls_frame, text="Dátum:").grid(row=1, column=0)
datum_cal = Calendar(fgls_frame, selectmode="day", year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
datum_cal.grid(row=1, column=1)

fgls_gomb = Button(fgls_frame, text="Foglalás", command=fgls_gomb_click)
fgls_gomb.grid(row=2, column=0, columnspan=2, pady=5)

# Lemondás rész
lemond_frame = LabelFrame(ablak, text="Lemondás")
lemond_frame.grid(row=0, column=1, padx=10, pady=10)

Label(lemond_frame, text="Szobaszám:").grid(row=0, column=0)
szobsz_lemond_entry = Entry(lemond_frame)
szobsz_lemond_entry.grid(row=0, column=1)

Label(lemond_frame, text="Dátum:").grid(row=1, column=0)
datum_lemond_cal = Calendar(lemond_frame, selectmode="day", year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
datum_lemond_cal.grid(row=1, column=1)

lemond_gomb = Button(lemond_frame, text="Lemondás", command=lemond_gomb_click)
lemond_gomb.grid(row=2, column=0, columnspan=2, pady=5)

# Foglalások listázása rész
listaz_gomb = Button(ablak, text="Foglalások listázása", command=listaz_gomb_click)
listaz_gomb.grid(row=1, column=0, columnspan=2, pady=10)

ablak.mainloop()