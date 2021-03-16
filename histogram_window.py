from tkinter import Label, Toplevel
from tkinter.constants import S
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from numpy import amax

#Dodać dla kolorowych
class NewHistogramWindow(Toplevel):
    def __init__(self, image, name, master = None): 
        super().__init__(master = master)
        self.set_basic(image, name)

        self.create_hist_value_display()  
        self.create_cavas()  

        self.p = self.f.gca()      
        self.update_histogram(image)
        

    def mouse_move(self, event):
        if event.xdata is not None:
            self.xData.config(text=round(event.xdata))
            if self.image.isGrayScale:
                self.yData.config(text=self.image.lut[round(event.xdata)])
            else:
                self.yData.config(text="({}, {}, {})".format(int(self.image.lut[round(event.xdata)][0]), int(self.image.lut[round(event.xdata)][1]), int(self.image.lut[round(event.xdata)][2])))


    def create_hist_value_display(self):
        xLabel = Label(self.histogramPanel, text="Value:")
        xLabel.place(relwidth=0.2, height=40, relx=0.2, rely=0.99, anchor=S)
        self.xData = Label(self.histogramPanel, text='')
        self.xData.place(relwidth = 0.1, height = 40, relx=0.3, rely=0.99, anchor=S)


        yLabel = Label(self.histogramPanel, text="Count:")
        yLabel.place(relwidth=0.15, height=40, relx=0.45, rely=0.99, anchor=S)
        self.yData = Label(self.histogramPanel, text='')
        self.yData.place(relwidth = 0.2, height = 40, relx=0.6, rely=0.99, anchor=S)
        

    def update_histogram(self, image):
        if image.isGrayScale:
            self.p.hist([i for i in range(256)], weights=image.lut, density=False, bins = [i for i in range(256)], color='black')
        else:
            self.p.hist([i for i in range(256)], weights=image.lut[:,0], density=False, bins = [i for i in range(256)], color='red')
            self.p.hist([i for i in range(256)], weights=image.lut[:,1], density=False, bins = [i for i in range(256)], color='green')
            self.p.hist([i for i in range(256)], weights=image.lut[:,2], density=False, bins = [i for i in range(256)], color='blue')
        self.set_axis()
            
        

    def set_axis(self):
        self.p.axis([0, 255, 0, int(amax(self.image.lut))])
        self.p.set_yticklabels([0, int(amax(self.image.lut))])
        self.p.set_yticks([0, int(amax(self.image.lut))])   
        self.p.set_xticklabels([0, 255])
        self.p.set_xticks([0, 255])

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