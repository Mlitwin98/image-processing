from tkinter import Toplevel, Label
from numpy import transpose, array, arange
from skimage import draw
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class NewLineProfileWindow(Toplevel):
    def __init__(self, name, lineCoords, master = None): 
        super().__init__(master = master)
        self.title("Linia profilu {}".format(name))
        self.minsize(800, 500)
        #self.visibleImageRes = visibleImageRes
        
        self.set_figures()
        self.update_line(lineCoords)
        self.p.set_xlabel('Pixel')
        self.p.set_ylabel('Wartość')
        self.protocol("WM_DELETE_WINDOW", lambda: self.report_close_to_master())
    
    def set_figures(self):
        self.plotPanel = Label(self)
        self.plotPanel.place(relwidth=1, relheight = 1, x=0, y=0)
        self.f = Figure(tight_layout=True)
        self.canvas = FigureCanvasTkAgg(self.f, master=self.plotPanel)
        self.canvas.get_tk_widget().place(relwidth=1, relheight = 1, x=0, y=0)
        self.p = self.f.gca()

    def update_line(self, lineCoords):
        self.p.clear()
        self.line = transpose(array(draw.line(lineCoords['x'], lineCoords['y'], lineCoords['x2'], lineCoords['y2'])))
        self.line = self.line[self.line[:, 1] < self.master.image.cv2Image.shape[1]]
        self.line = self.line[self.line[:, 0] < self.master.image.cv2Image.shape[0]]
        if self.master.image.isGrayScale:
            self.data = self.master.image.cv2Image.copy()[self.line[:, 1], self.line[:, 0]]
            self.p.plot(self.data, color='black')
        else:
            self.data = self.master.image.cv2Image.copy()[self.line[:, 1], self.line[:, 0], :]
            self.p.plot(self.data[:, 0], 'r', self.data[:, 1], 'g', self.data[:, 2], 'b')
        self.p.axis([0, len(self.data)-1, 0, 255])
        self.p.set_xticks(arange(0, self.data.shape[0], self.data.shape[0]-1))
        self.p.set_yticks(arange(0, 256, 15))
        self.canvas.draw()

    def report_close_to_master(self):
        self.master.profileWindow = None
        self.destroy()
    