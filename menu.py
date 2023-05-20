import tkinter as tk
from PIL import Image, ImageTk

import couchdb
from dashboard import Dashboard
from eingabe import Eingabe
from table import Table


class Menu:

    def __init__(self):
        root = tk.Tk()
        self.root = root
        root.title("Menü")
        root.geometry('500x500')

        self.show_images()

        title_label = tk.Label(root, text="Baumdatenbank", font=("TkDefaultFont", 24))
        title_label.place(x=100, y=175, width=300, height=40)

        dashboard_button = tk.Button(root, text="Dashboard", command=self.dashboard, font=("TkDefaultFont", 14))
        dashboard_button.place(x=150, y=250, width=200, height=40)

        eingabe_button = tk.Button(root, text="Eingabeformular", command=self.eingabe, font=("TkDefaultFont", 14))
        eingabe_button.place(x=150, y=300, width=200, height=35)

        table_button = tk.Button(root, text="Bäume auflisten", command=self.table, font=("TkDefaultFont", 14))
        table_button.place(x=150, y=350, width=200, height=35)

        root.mainloop()

    def eingabe(self):
        Eingabe(self.root)

    def table(self):
        couch = couchdb.CouchDB()
        doc = couch.get_all_documents("trees")
        doc = couch.remove_design_documents(doc)
        table = Table(self.root, doc)

    def dashboard(self):
        Dashboard(self.root)

    def show_images(self):
        cdb_image = Image.open("assets/Apache_CouchDB_logo.png")
        cdb_image = cdb_image.resize((75, 75), Image.ANTIALIAS)
        cdb_photo = ImageTk.PhotoImage(cdb_image)
        cdb_label = tk.Label(self.root, image=cdb_photo)
        cdb_label.image = cdb_photo
        cdb_label.place(x=212, y=90)

        scale = 5
        hs_image = Image.open("assets/Logo_Hochschule_Trier.png")
        hs_image = hs_image.resize((int(56*scale), int(13*scale)), Image.ANTIALIAS)
        hs_photo = ImageTk.PhotoImage(hs_image)
        hs_label = tk.Label(self.root, image=hs_photo)
        hs_label.image = hs_photo
        hs_label.place(x=500-hs_image.width, y=0)

