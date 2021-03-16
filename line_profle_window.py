from tkinter import Toplevel, Label
from numpy import transpose, array
from skimage import draw
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class NewLineProfileWindow(Toplevel):
    def __init__(self, image, name, lineCoords, visibleImageRes, master = None): 
        super().__init__(master = master)
        self.image = image
        self.title("Linia profilu {}".format(name))
        self.minsize(800, 500)
        self.visibleImageRes = visibleImageRes
        self.plotPanel = Label(self)
        self.plotPanel.place(relwidth=1, relheight = 1, x=0, y=0)


        self.f = Figure(tight_layout=True)
        self.canvas = FigureCanvasTkAgg(self.f, master=self.plotPanel)
        self.canvas.get_tk_widget().place(relwidth=1, relheight = 1, x=0, y=0)
        
        self.p = self.f.gca()
        self.update_line(lineCoords, image)
        self.p.set_xlabel('Pixel')
        self.p.set_ylabel('Wartość')
        
    def update_line(self, lineCoords, image):
        self.p.clear()
        self.line = transpose(array(draw.line(lineCoords['x'], lineCoords['y'], lineCoords['x2'], lineCoords['y2'])))
        if image.isGrayScale:
            self.data = image.cv2Image.copy()[self.line[:, 1], self.line[:, 0]]
            self.p.plot(self.data, color='black')
            self.p.axis([0, len(self.data)-1, 0, 255])
        else:
            self.data = image.cv2Image.copy()[self.line[:, 1], self.line[:, 0], :]
            self.p.plot(self.data[:, 0], 'b', self.data[:, 1], 'g', self.data[:, 2], 'r')
            self.p.axis([0, len(self.data)-1, 0, 255])
        self.canvas.draw()