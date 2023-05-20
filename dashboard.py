import math
import tkinter as tk

import couchdb
from eingabe import Eingabe
from tkinter import ttk


class Dashboard:

    def __init__(self, tkroot):
        root = tk.Toplevel(tkroot)
        self.root = root
        root.title("Dashboard")
        width = 1010
        height = 365
        root.geometry(f'{width}x{height}')
        root.resizable(False, False)

        self.couch = couchdb.CouchDB()

        frame_age_avg = tk.Frame(root)
        frame_age_avg.place(x=0, y=40, width=width/2, height=height-40)

        frame_gesundheit = tk.Frame(root)
        frame_gesundheit.place(x=510, y=40, width=width/4, height=height - 40)

        frame_standort = tk.Frame(root)
        frame_standort.place(x=770, y=40, width=width/4, height=height - 40)

        tk.Label(root, text="Altersstatistiken", font=("TkDefaultFont", 14), anchor="w").place(x=10, y=10, width=200, height=20)
        tk.Label(root, text="Gesundheitszustände", font=("TkDefaultFont", 14), anchor="w").place(x=510, y=10, width=200, height=20)
        tk.Label(root, text="Standorte", font=("TkDefaultFont", 14), anchor="w").place(x=770, y=10, width=200, height=20)

        self.age_avg = self.init_age_avg_treeview(frame_age_avg, width/2, height)
        self.gesundheit = self.init_gesundheit_treeview(frame_gesundheit, width/4, height)
        self.standort = self.init_standort_treeview(frame_standort, width/4, height)

        self.avg_age_load()
        self.gesundheit_load()
        self.standort_load()

    def init_age_avg_treeview(self, frame, width, height):
        age_avg = ttk.Treeview(frame, selectmode='browse')
        age_avg.place(x=0, y=0, width=width)
        age_avg['columns'] = ('art', 'anzahl', 'summe', 'min', 'max', 'avg')

        column_width = math.floor(width / 6)

        age_avg.column("#0", width=0, stretch=tk.NO)
        age_avg.column("art", anchor=tk.CENTER, width=column_width)
        age_avg.column("anzahl", anchor=tk.CENTER, width=column_width)
        age_avg.column("summe", anchor=tk.CENTER, width=column_width)
        age_avg.column("min", anchor=tk.CENTER, width=column_width)
        age_avg.column("max", anchor=tk.CENTER, width=column_width)
        age_avg.column("avg", anchor=tk.CENTER, width=column_width)

        age_avg.heading("#0", text="", anchor=tk.CENTER)
        age_avg.heading("art", text="Art", anchor=tk.CENTER)
        age_avg.heading("anzahl", text="Anzahl", anchor=tk.CENTER)
        age_avg.heading("summe", text="Summe", anchor=tk.CENTER)
        age_avg.heading("min", text="Minimum", anchor=tk.CENTER)
        age_avg.heading("max", text="Maximum", anchor=tk.CENTER)
        age_avg.heading("avg", text="Durchschnitt", anchor=tk.CENTER)

        return age_avg

    def avg_age_load(self):
        self.age_avg.delete(*self.age_avg.get_children())
        avg_age = self.couch.get_view("trees", "dashboard", "avgage", True)
        if avg_age is None:
            return
        for row in avg_age["rows"]:
            self.age_avg.insert(parent='', index='end', text='',
                                values=(row["key"],
                                        row["value"].get("count", 0),
                                        row["value"].get("sum", 0),
                                        row["value"].get("min", 0),
                                        row["value"].get("max", 0),
                                        row["value"].get("sum", 0)/row["value"].get("count", 0)))

    def init_gesundheit_treeview(self, frame, width, height):
        gesundheit = ttk.Treeview(frame, selectmode='browse')
        gesundheit.place(x=0, y=0, width=width)
        gesundheit['columns'] = ('gesundheit', 'anzahl')

        column_width = math.floor(width / 2)

        gesundheit.column("#0", width=0, stretch=tk.NO)
        gesundheit.column("gesundheit", anchor=tk.CENTER, width=column_width)
        gesundheit.column("anzahl", anchor=tk.CENTER, width=column_width)

        gesundheit.heading("#0", text="", anchor=tk.CENTER)
        gesundheit.heading("gesundheit", text="Gesundheitszustand", anchor=tk.CENTER)
        gesundheit.heading("anzahl", text="Anzahl", anchor=tk.CENTER)

        return gesundheit

    def gesundheit_load(self):
        self.gesundheit.delete(*self.gesundheit.get_children())
        gesundheit_data = self.couch.get_view("trees", "dashboard", "gesundheit", True)
        if gesundheit_data is None:
            return
        for row in gesundheit_data["rows"]:
            self.gesundheit.insert(parent='', index='end', text='', values=(row["key"], row["value"]))

    def init_standort_treeview(self, frame, width, height):
        standort = ttk.Treeview(frame, selectmode='browse')
        standort.place(x=0, y=0, width=width)
        standort['columns'] = ('standort', 'anzahl')

        column_width = math.floor(width / 2)

        standort.column("#0", width=0, stretch=tk.NO)
        standort.column("standort", anchor=tk.CENTER, width=column_width)
        standort.column("anzahl", anchor=tk.CENTER, width=column_width)

        standort.heading("#0", text="", anchor=tk.CENTER)
        standort.heading("standort", text="Standort", anchor=tk.CENTER)
        standort.heading("anzahl", text="Anzahl", anchor=tk.CENTER)

        return standort

    def standort_load(self):
        self.standort.delete(*self.standort.get_children())
        standort_data = self.couch.get_view("trees", "dashboard", "standort", True)
        if standort_data is None:
            return
        for row in standort_data["rows"]:
            self.standort.insert(parent='', index='end', text='', values=(row["key"], row["value"]))

