import math
import tkinter as tk

import couchdb
from eingabe import Eingabe
from tkinter import ttk


class Table:

    def __init__(self, tkroot, documents):
        root = tk.Toplevel(tkroot)
        self.root = root
        root.title("Bäume auflisten")
        width = 1000
        height = 365
        root.geometry(f'{width}x{height}')
        root.resizable(False, False)

        self.documents = documents
        self.couch = couchdb.CouchDB()

        frame = tk.Frame(root)
        frame.place(width=width)
        frame.pack()

        trees = ttk.Treeview(frame, selectmode='browse')
        trees.place(width=width)
        self.trees = trees
        trees['columns'] = ('art', 'notiz', 'timestamp', 'alter', 'gesundheit', 'standort', 'bild')

        trees.column("#0", width=0, stretch=tk.NO)
        trees.column("art", anchor=tk.CENTER, width=math.floor(width/7))
        trees.column("notiz", anchor=tk.CENTER, width=math.floor(width/7))
        trees.column("timestamp", anchor=tk.CENTER, width=math.floor(width/7))
        trees.column("alter", anchor=tk.CENTER, width=math.floor(width/7))
        trees.column("gesundheit", anchor=tk.CENTER, width=math.floor(width/7))
        trees.column("standort", anchor=tk.CENTER, width=math.floor(width/7))
        trees.column("bild", anchor=tk.CENTER, width=math.floor(width/7))

        trees.heading("#0", text="", anchor=tk.CENTER)
        trees.heading("art", text="Art", anchor=tk.CENTER)
        trees.heading("notiz", text="Notiz", anchor=tk.CENTER)
        trees.heading("timestamp", text="Zeitpunkt", anchor=tk.CENTER)
        trees.heading("alter", text="Alter", anchor=tk.CENTER)
        trees.heading("gesundheit", text="Gesundheitszustand", anchor=tk.CENTER)
        trees.heading("standort", text="Standort", anchor=tk.CENTER)
        trees.heading("bild", text="Bild", anchor=tk.CENTER)

        self.doc_insert(documents)

        trees.pack()

        tk.Label(root, text="Art", font=("TkDefaultFont", 10)).place(x=500, y=240, width=200, height=20)
        self.art_entry = tk.Entry(root)
        self.art_entry.place(x=500, y=260, width=200, height=20)

        tk.Label(root, text="Alter", font=("TkDefaultFont", 10)).place(x=500, y=280, width=200, height=20)
        self.alter_entry = tk.Entry(root)
        self.alter_entry.place(x=500, y=300, width=200, height=20)

        tk.Label(root, text="Gesundheitszustand", font=("TkDefaultFont", 10)).place(x=710, y=240, width=200, height=20)
        self.gesundheit_entry = tk.Entry(root)
        self.gesundheit_entry.place(x=710, y=260, width=200, height=20)

        tk.Label(root, text="Standort", font=("TkDefaultFont", 10)).place(x=710, y=280, width=200, height=20)
        self.standort_entry = tk.Entry(root)
        self.standort_entry.place(x=710, y=300, width=200, height=20)

        filter_button = tk.Button(root, text="Filtern", command=self.doc_filter, font=("TkDefaultFont", 12))
        filter_button.place(x=605, y=330, width=200, height=20)

        edit_button = tk.Button(root, text="Bearbeiten", command=self.doc_edit, font=("TkDefaultFont", 14))
        edit_button.place(x=150, y=250, width=200, height=40)

        refresh_button = tk.Button(root, text="Aktualisieren", command=self.doc_refresh, font=("TkDefaultFont", 14))
        refresh_button.place(x=150, y=300, width=200, height=40)

    def doc_insert(self, documents):
        self.trees.delete(*self.trees.get_children())
        i = 0
        for doc in documents:
            print(doc)
            self.trees.insert(parent='', index='end', iid=i, text='',
                              values=(doc.content.get("art", ""),
                                      doc.content.get("notiz", "").replace("\n", ""),
                                      doc.content.get("timestamp", ""),
                                      doc.content.get("alter", ""),
                                      doc.content.get("gesundheitszustand", ""),
                                      doc.content.get("standort", ""),
                                      doc.content.get("bild", "")))
            i += 1

    def doc_edit(self):
        selected = self.trees.focus()
        if selected != '':
            Eingabe(self.root, self.documents[int(selected)])

    def doc_refresh(self):
        self.art_entry.delete(0, 'end')
        self.alter_entry.delete(0, 'end')
        self.gesundheit_entry.delete(0, 'end')
        self.standort_entry.delete(0, 'end')

        doc = self.couch.get_all_documents("trees")
        doc = self.couch.remove_design_documents(doc)
        self.doc_insert(doc)

    def doc_filter(self):
        art = self.art_entry.get()
        alter = self.alter_entry.get()
        gesundheit = self.gesundheit_entry.get()
        standort = self.standort_entry.get()
        filters = {"art": art, "alter": alter, "gesundheitszustand": gesundheit, "standort": standort}
        docs = self.couch.find_all_eq_documents("trees", filters)
        self.doc_insert(docs)

