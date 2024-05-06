from tkinter import *
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime
import winsound

class Szoba:
    def __init__(self, szobsz, ar):
        self.szobsz = szobsz
        self.ar = ar

class EgyagyasSzoba(Szoba):
    def __init__(self, szobsz, bath):
        super().__init__(szobsz, 70000)
        self.bath = bath

class KetagyasSzoba(Szoba):
    def __init__(self, szobsz, extra):
        super().__init__(szobsz, 90000)
        self.extra = extra

class Foglalas:
    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum

class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.fgs_ok = []

    def add_szoba(self, szoba):
        self.szobak.append(szoba)

    def fgs(self, szobsz, datum):
        for fgs in self.fgs_ok:
            if fgs.szoba.szobsz == szobsz and fgs.datum == datum:
                return False
        for szoba in self.szobak:
            if szoba.szobsz == szobsz:
                self.fgs_ok.append(Foglalas(szoba, datum))
                return szoba.ar
        return False

    def lmond(self, szobsz, datum):
        for fgs in self.fgs_ok:
            if fgs.szoba.szobsz == szobsz and fgs.datum == datum:
                self.fgs_ok.remove(fgs)
                return True
        return False

    def list_fgs_ok(self):
        return [f"Szoba: {fgs.szoba.szobsz}, Időpont: {fgs.datum}" for fgs in self.fgs_ok]

def foglalas_clicked():
    szobsz = szobsz_entry.get()
    datum_str = datum_entry.get()
    try:
        datum = datetime.strptime(datum_str, "%Y-%m-%d")
        if datum < datetime.now():
            status_label.config(text="Hibás dátum! A foglalás csak jövőbeni időpontra lehetséges.")
            winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
        else:
            ar = hotel.fgs(szobsz, datum)
            if ar:
                status_label.config(text=f"A foglalás sikeres! Az ár: {ar} Ft")
            else:
                status_label.config(text="Hibás szobaszám!")
                winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
    except ValueError:
        status_label.config(text="Hibás dátum formátum!")
        winsound.PlaySound("SystemHand", winsound.SND_ALIAS)

def lemondas_clicked():
    szobsz = szobsz_lemondas_entry.get()
    datum_str = datum_lemondas_entry.get()
    try:
        datum = datetime.strptime(datum_str, "%Y-%m-%d")
        if hotel.lmond(szobsz, datum):
            status_label.config(text="A foglalás sikeresen lemondva.")
        else:
            status_label.config(text="Nincs ilyen foglalás.")
            winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
    except ValueError:
        status_label.config(text="Hibás dátum formátum!")
        winsound.PlaySound("SystemHand", winsound.SND_ALIAS)

def listaz_clicked():
    foglalas_listbox.delete(0, END)
    for item in hotel.list_fgs_ok():
        foglalas_listbox.insert(END, item)

# Rendszer feltöltés: Szalloda létrehozása
hotel = Szalloda("Pihenő Hotel")

# Rendszer feltöltés: Szobák hozzáadása
hotel.add_szoba(EgyagyasSzoba("101", "Kád"))
hotel.add_szoba(EgyagyasSzoba("102", "Zuhany"))
hotel.add_szoba(KetagyasSzoba("201", "Jacuzzi"))

# GUI létrehozása
root = Tk()
root.title("Szobafoglalás")

foglalas_frame = LabelFrame(root, text="Foglalás")
foglalas_frame.grid(row=0, column=0, padx=10, pady=10)

szobsz_label = Label(foglalas_frame, text="Szobaszám:")
szobsz_label.grid(row=0, column=0, padx=5, pady=5)
szobsz_entry = Entry(foglalas_frame)
szobsz_entry.grid(row=0, column=1, padx=5, pady=5)

datum_label = Label(foglalas_frame, text="Dátum (ÉÉÉÉ-HH-NN):")
datum_label.grid(row=1, column=0, padx=5, pady=5)
datum_entry = Entry(foglalas_frame)
datum_entry.grid(row=1, column=1, padx=5, pady=5)

foglalas_button = Button(foglalas_frame, text="Foglalás", command=foglalas_clicked)
foglalas_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

lemondas_frame = LabelFrame(root, text="Lemondás")
lemondas_frame.grid(row=0, column=1, padx=10, pady=10)

szobsz_lemondas_label = Label(lemondas_frame, text="Szobaszám:")
szobsz_lemondas_label.grid(row=0, column=0, padx=5, pady=5)
szobsz_lemondas_entry = Entry(lemondas_frame)
szobsz_lemondas_entry.grid(row=0, column=1, padx=5, pady=5)

datum_lemondas_label = Label(lemondas_frame, text="Dátum (ÉÉÉÉ-HH-NN):")
datum_lemondas_label.grid(row=1, column=0, padx=5, pady=5)
datum_lemondas_entry = Entry(lemondas_frame)
datum_lemondas_entry.grid(row=1, column=1, padx=5, pady=5)

lemondas_button = Button(lemondas_frame, text="Lemondás", command=lemondas_clicked)
lemondas_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

foglalasok_frame = LabelFrame(root, text="Foglalások")
foglalasok_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

foglalas_listbox = Listbox(foglalasok_frame, width=50)
foglalas_listbox.grid(row=0, column=0, padx=5, pady=5)

listaz_button = Button(foglalasok_frame, text="Foglalások listázása", command=listaz_clicked)
listaz_button.grid(row=1, column=0, padx=5, pady=5)

status_label = Label(root, text="")
status_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()