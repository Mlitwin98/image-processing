from tkinter import Canvas, Toplevel, Menu
from tkinter.constants import DISABLED, LEFT, NW, NORMAL
from PIL import Image, ImageTk
from image_saved import ImageSaved
from histogram_window import NewHistogramWindow
from lut_window import NewLutWindow
from line_profle_window import NewLineProfileWindow

class NewImageWindow(Toplevel):
    def __init__(self, master = None, pathToImage = None, name=None): 
        super().__init__(master = master)

        self.set_images(pathToImage)
        self.set_geometry()
        self.set_basic(master, pathToImage, name)
        self.place_menu()
        self.manage_line_profile()
        self.bind_functions()

    @staticmethod
    def duplicate_window(master, pathToImage,  name):
        NewImageWindow(master, pathToImage, name)

    def resize_img(self, event):
        self.newWidth = event.width
        self.newHeight = event.height
        self.imageFromArray = self.imageCopy.resize((self.newWidth, self.newHeight))
        self.photoImage = ImageTk.PhotoImage(self.imageFromArray)
        self.imagePanel.create_image(0, 0, anchor=NW, image=self.photoImage)

    def set_geometry(self):
        self.geometry('{}x{}'.format(self.imageFromArray.width, self.imageFromArray.height))
        self.minsize(200, 200)

    def place_menu(self):
        self.topMenu = Menu()
        self.topMenu.add_command(label='LUT', compound=LEFT, command= lambda: NewLutWindow(self.image, self.name, self))
        self.topMenu.add_command(label='Histogram', compound=LEFT, command= lambda: NewHistogramWindow(self.image, self.name, self))
        self.topMenu.add_command(label='Linia profilu', compound=LEFT, state=DISABLED, command= lambda: NewLineProfileWindow(self.image, self.name, self.lineCoords, [self.newWidth, self.newHeight], self))
        self.config(menu = self.topMenu)

    def bind_functions(self):
        self.bind('<Configure>', self.resize_img)
        self.bind('<Control-d>', lambda event: NewImageWindow.duplicate_window(self.master, self.path, self.name + '(Kopia)'))
        self.bind("<ButtonPress-3>", self.click)
        self.bind("<B3-Motion>", self.drag)

    def set_images(self, pathToImage):
        self.image = ImageSaved(pathToImage)
        self.imageFromArray = Image.fromarray(self.image.cv2Image)
        self.imageCopy = self.imageFromArray.copy()

    def set_basic(self, master, pathToImage, name):
        self.focus_force()
        self.master = master
        self.path = pathToImage
        self.name = name 
        self.title(name) 
        self.imagePanel = Canvas(self)
        self.imagePanel.place(relwidth=1, relheight = 1, x=0, y=0)

    def manage_line_profile(self):
        self.lineCoords = {"x":0,"y":0,"x2":0,"y2":0}
        self.line = None

    def click(self, e):
        self.lineCoords["x"] = e.x
        self.lineCoords["y"] = e.y
        self.topMenu.entryconfigure('Linia profilu', state=NORMAL)

    def drag(self, e):
        self.lineCoords["x2"] = e.x
        self.lineCoords["y2"] = e.y
        if self.line is not None:
            self.imagePanel.delete(self.line) 
        self.line = self.imagePanel.create_line(self.lineCoords["x"], self.lineCoords["y"], self.lineCoords['x2'], self.lineCoords['y2'], fill='red', dash=(2, 2))