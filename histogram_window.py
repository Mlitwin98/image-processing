import tkinter as tk
from tkinter import Toplevel
import matplotlib as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class NewHistogramWindow(Toplevel):
    def __init__(self, image, name, master = None): 
        super().__init__(master = master)
        self.image = image
        self.histogramPanel = tk.Label(self)
        self.histogramPanel.place(relwidth=1, relheight = 1, x=0, y=0)
        self.title("Histogram {}".format(name))
        self.minsize(400, 400)

        f = Figure(figsize=(5,4), dpi=100)
        canvas = FigureCanvasTkAgg(f, master=self.histogramPanel)
        canvas.get_tk_widget().place(relwidth=1, relheight = 0.95, x=0, y=0)
        p = f.gca()
        p.hist([i for i in range(256)], weights=image.lut, density=False, bins = [i for i in range(256)], color='black')
        f.tight_layout()
        p.axis([0, 256, 0, max(image.lut)+50])