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

        line = transpose(array(draw.line(lineCoords['x'], lineCoords['y'], lineCoords['x2'], lineCoords['y2'])))
        self.data = image.cv2Image.copy()[line[:, 1], line[:, 0]]

        self.f = Figure(tight_layout=True)
        canvas = FigureCanvasTkAgg(self.f, master=self.plotPanel)
        #canvas.mpl_connect('motion_notify_event', self.mouse_move)
        canvas.get_tk_widget().place(relwidth=1, relheight = 0.9, x=0, y=0)
        p = self.f.gca()
        p.plot(self.data)