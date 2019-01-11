import tkinter as tk
from __main__ import *

class SharedTool(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand= True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        frame = StartPage(container, self)
        
        self.frames[StartPage] = frame
        frame.grid(row=0, column = 0, sticky="nsew")

        self.show_frame(StarPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
