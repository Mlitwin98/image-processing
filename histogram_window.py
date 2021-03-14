from tkinter import Label, Toplevel
from tkinter.constants import S
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from math import floor

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
            self.xData.config(text=floor(event.xdata))
            self.yData.config(text=self.image.lut[floor(event.xdata)])


    def create_hist_value_display(self):
        xLabel = Label(self.histogramPanel, text="Value:")
        xLabel.place(relwidth=0.2, height=40, relx=0.2, rely=0.99, anchor=S)
        self.xData = Label(self.histogramPanel, text='')
        self.xData.place(relwidth = 0.1, height = 40, relx=0.3, rely=0.99, anchor=S)


        yLabel = Label(self.histogramPanel, text="Count:")
        yLabel.place(relwidth=0.2, height=40, relx=0.5, rely=0.99, anchor=S)
        self.yData = Label(self.histogramPanel, text='')
        self.yData.place(relwidth = 0.1, height = 40, relx=0.6, rely=0.99, anchor=S)
        

    def update_histogram(self, image):
        p = self.f.gca()
        p.hist([i for i in range(256)], weights=image.lut, density=False, bins = [i for i in range(256)], color='black')
        p.axis([0, 255, 0, max(image.lut)])
        p.set_yticklabels([0, max(image.lut)])
        p.set_yticks([0, max(image.lut)])
        p.set_xticklabels([0, 255])
        p.set_xticks([0, 255])

    def create_cavas(self):
        self.f = Figure(tight_layout=True)
        canvas = FigureCanvasTkAgg(self.f, master=self.histogramPanel)
        canvas.mpl_connect('motion_notify_event', self.mouse_move)
        canvas.get_tk_widget().place(relwidth=1, relheight = 0.9, x=0, y=0)

    def set_basic(self, image, name):
        self.image = image
        self.histogramPanel = Label(self)
        self.histogramPanel.place(relwidth=1, relheight = 1, x=0, y=0)
        self.title("Histogram {}".format(name))
        self.minsize(800, 500)