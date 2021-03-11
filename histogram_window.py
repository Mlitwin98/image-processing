import tkinter as tk
from tkinter import Toplevel
from tkinter.constants import DISABLED, NORMAL
import matplotlib as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

#Dodać dla kolorowych
class NewHistogramWindow(Toplevel):
    def __init__(self, image, name, master = None): 
        super().__init__(master = master)
        self.set_basic(image, name)

        self.create_hist_value_display()  
        self.create_cavas()        
        self.update_histogram(image)


    def mouse_move(self, event):
        if event.xdata is not None:
            self.xData.config(text=math.floor(event.xdata))
            self.yData.config(text=self.image.lut[math.floor(event.xdata)])


    def create_hist_value_display(self):
        xLabel = tk.Label(self.histogramPanel, text="Value:")
        xLabel.place(relwidth=0.2, height=40, relx=0.2, rely=0.99, anchor=tk.S)
        self.xData = tk.Label(self.histogramPanel, text='')
        self.xData.place(relwidth = 0.1, height = 40, relx=0.3, rely=0.99, anchor=tk.S)


        yLabel = tk.Label(self.histogramPanel, text="Count:")
        yLabel.place(relwidth=0.2, height=40, relx=0.5, rely=0.99, anchor=tk.S)
        self.yData = tk.Label(self.histogramPanel, text='')
        self.yData.place(relwidth = 0.1, height = 40, relx=0.6, rely=0.99, anchor=tk.S)
        

    def update_histogram(self, image):
        self.p = self.f.gca()
        self.p.hist([i for i in range(256)], weights=image.lut, density=False, bins = [i for i in range(256)], color='black')
        self.p.axis([0, 256, 0, max(image.lut)])
        self.p.set_yticklabels([0, max(image.lut)])
        self.p.set_yticks([0, max(image.lut)])
        self.p.set_xticklabels([0, 256])
        self.p.set_xticks([0, 256])

    def create_cavas(self):
        self.f = Figure(tight_layout=True)
        canvas = FigureCanvasTkAgg(self.f, master=self.histogramPanel)
        canvas.mpl_connect('motion_notify_event', self.mouse_move)
        canvas.get_tk_widget().place(relwidth=1, relheight = 0.9, x=0, y=0)

    def set_basic(self, image, name):
        self.image = image
        self.histogramPanel = tk.Label(self)
        self.histogramPanel.place(relwidth=1, relheight = 1, x=0, y=0)
        self.title("Histogram {}".format(name))
        self.minsize(800, 500)