import tkinter as tk
from tkinter import filedialog
import datetime

from PIL import ImageTk, Image

import couchdb
from image import ImageShow


class Eingabe:

    def __init__(self, tkroot, document=None):
        root = tk.Toplevel(tkroot)
        self.root = root
        root.title("Eingabeformular")
        root.geometry('600x525')
        root.resizable(False, False)

        self.document = document
        self.couch = couchdb.CouchDB()
        self.image = None

        tk.Label(root, text="Art").place(x=200, y=20, width=200, height=20)
        self.art_entry = tk.Entry(root)
        self.art_entry.place(x=200, y=40, width=200, height=20)

        tk.Label(root, text="Notiz").place(x=200, y=60, width=200, height=20)
        self.notiz_entry = tk.Text(root)
        self.notiz_entry.place(x=200, y=80, width=200, height=50)

        tk.Label(root, text="Alter").place(x=200, y=130, width=200, height=20)
        self.alter_entry = tk.Entry(root)
        self.alter_entry.place(x=200, y=150, width=200, height=20)

        tk.Label(root, text="Gesundheitszustand").place(x=200, y=170, width=200, height=20)
        self.gesundheit_entry = tk.Entry(root)
        self.gesundheit_entry.place(x=200, y=190, width=200, height=20)

        tk.Label(root, text="Standort").place(x=200, y=210, width=200, height=20)
        self.standort_entry = tk.Entry(root)
        self.standort_entry.place(x=200, y=230, width=200, height=20)

        tk.Label(root, text="Bild (optional)").place(x=200, y=250, width=200, height=20)
        self.bild_var = tk.StringVar(root)
        self.bild_button = tk.Button(root, text="Bild öffnen", command=self.open_image)
        self.bild_button.place(x=200, y=270, width=200, height=20)

        self.bild_label = tk.Label(root)
        self.bild_label.bind("<Button-1>", self.show_image)
        self.bild_label.place(x=150, y=290, width=300, height=100)

        speichern_button = tk.Button(root, text="Speichern", command=self.speichern, font=("TkDefaultFont", 12))
        speichern_button.place(x=200, y=420, width=200, height=40)

        if document is not None:
            self.art_entry.insert('end', document.content.get("art", ""))
            self.notiz_entry.insert('end', document.content.get("notiz", ""))
            self.alter_entry.insert('end', document.content.get("alter", ""))
            self.gesundheit_entry.insert('end', document.content.get("gesundheitszustand", ""))
            self.standort_entry.insert('end', document.content.get("standort", ""))
            self.bild_label.config(text=document.content.get("bild", ""))
            self.bild_var.set(document.content.get("bild", ""))
            image = self.couch.get_attachment(document)
            if image is not None:
                self.load_image(image)

            delete_button = tk.Button(root, text="Löschen", command=self.loeschen, font=("TkDefaultFont", 12))
            delete_button.place(x=200, y=460, width=200, height=30)
            delete_button["fg"] = "#ff0000"

    def speichern(self):
        art = self.art_entry.get()
        notiz = self.notiz_entry.get(1.0, 'end')
        timestamp = f"{datetime.datetime.now():%d-%m-%Y %H:%M:%S%z}"
        alter = self.alter_entry.get()
        gesundheit = self.gesundheit_entry.get()
        standort = self.standort_entry.get()
        bild = self.bild_var.get()
        print(f"Art: {art}\nNotiz: {notiz}\nTimestamp: {timestamp}\nAlter: {alter}\nGesundheitszustand: {gesundheit}\nStandort: {standort}\nBild: {bild}")
        payload = {"art": art, "notiz": notiz, "timestamp": timestamp, "alter": alter, "gesundheitszustand": gesundheit, "standort": standort, "bild": bild}

        if self.document is not None:
            doc = self.couch.update_doc(self.document, payload)
        else:
            doc = self.couch.insert("trees", payload)

        # Im Falle eines Bildes wird es hinzugefügt
        if len(self.bild_var.get()) > 1:
            self.couch.attachment(doc, self.bild_var.get())
        self.root.destroy()

    def loeschen(self):
        if self.document is not None:
            self.couch.delete(self.document)
        self.root.destroy()

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg")])
        if file_path:
            self.bild_var.set(file_path)
            self.bild_label.config(text=file_path)
            image = Image.open(file_path)
            self.load_image(image)

    def show_image(self, event):
        if self.image is not None:
            ImageShow(self.root, self.image)

    def load_image(self, image):
        thumbnail_image = image.copy()
        self.image = image
        thumbnail_image.thumbnail((100, 100))
        photo = ImageTk.PhotoImage(thumbnail_image)
        self.bild_label["image"] = photo
        self.bild_label.image = photo


