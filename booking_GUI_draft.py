from tkinter import *
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime

class Szoba:
    def __init__(self, szobaszam, ar):
        self.szobaszam = szobaszam
        self.ar = ar

class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(szobaszam, 5000)

class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(szobaszam, 8000)

class Foglalas:
    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum

class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = []

    def add_szoba(self, szoba):
        self.szobak.append(szoba)

    def foglalas(self, szobaszam, datum):
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                foglalas = Foglalas(szoba, datum)
                self.foglalasok.append(foglalas)
                return szoba.ar
        return None

    def lemondas(self, szobaszam, datum):
        for foglalas in self.foglalasok:
            if foglalas.szoba.szobaszam == szobaszam and foglalas.datum == datum:
                self.foglalasok.remove(foglalas)
                return True
        return False

    def listaz_foglalasok(self):
        foglalasok_str = ""
        for foglalas in self.foglalasok:
            foglalasok_str += f"Szoba: {foglalas.szoba.szobaszam}, Dátum: {foglalas.datum}\n"
        return foglalasok_str

def foglalas_gomb_click():
    szobaszam = szobaszam_entry.get()
    datum = datum_cal.selection_get()
    if datum:
        ar = hotel.foglalas(szobaszam, datum)
        if ar:
            messagebox.showinfo("Sikeres foglalás", f"A foglalás sikeres! Az ár: {ar} Ft")
        else:
            messagebox.showerror("Hiba", "Hibás szobaszám!")
    else:
        messagebox.showerror("Hiba", "Válassz egy dátumot!")

def lemondas_gomb_click():
    szobaszam = szobaszam_lemondas_entry.get()
    datum = datum_lemondas_cal.selection_get()
    if datum:
        sikeres = hotel.lemondas(szobaszam, datum)
        if sikeres:
            messagebox.showinfo("Sikeres lemondás", "A foglalás sikeresen lemondva.")
        else:
            messagebox.showerror("Hiba", "Nincs ilyen foglalás.")
    else:
        messagebox.showerror("Hiba", "Válassz egy dátumot!")

def listaz_gomb_click():
    foglalasok = hotel.listaz_foglalasok()
    if foglalasok:
        messagebox.showinfo("Foglalások listája", foglalasok)
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
foglalas_frame = LabelFrame(ablak, text="Foglalás")
foglalas_frame.grid(row=0, column=0, padx=10, pady=10)

Label(foglalas_frame, text="Szobaszám:").grid(row=0, column=0)
szobaszam_entry = Entry(foglalas_frame)
szobaszam_entry.grid(row=0, column=1)

Label(foglalas_frame, text="Dátum:").grid(row=1, column=0)
datum_cal = Calendar(foglalas_frame, selectmode="day", year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
datum_cal.grid(row=1, column=1)

foglalas_gomb = Button(foglalas_frame, text="Foglalás", command=foglalas_gomb_click)
foglalas_gomb.grid(row=2, column=0, columnspan=2, pady=5)

# Lemondás rész
lemondas_frame = LabelFrame(ablak, text="Lemondás")
lemondas_frame.grid(row=0, column=1, padx=10, pady=10)

Label(lemondas_frame, text="Szobaszám:").grid(row=0, column=0)
szobaszam_lemondas_entry = Entry(lemondas_frame)
szobaszam_lemondas_entry.grid(row=0, column=1)

Label(lemondas_frame, text="Dátum:").grid(row=1, column=0)
datum_lemondas_cal = Calendar(lemondas_frame, selectmode="day", year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
datum_lemondas_cal.grid(row=1, column=1)

lemondas_gomb = Button(lemondas_frame, text="Lemondás", command=lemondas_gomb_click)
lemondas_gomb.grid(row=2, column=0, columnspan=2, pady=5)

# Foglalások listázása rész
listaz_gomb = Button(ablak, text="Foglalások listázása", command=listaz_gomb_click)
listaz_gomb.grid(row=1, column=0, columnspan=2, pady=10)

ablak.mainloop()