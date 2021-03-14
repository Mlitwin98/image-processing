import tkinter as tk
from tkinter import Toplevel
from PIL import Image, ImageTk
from image_saved import ImageSaved
from histogram_window import NewHistogramWindow
from lut_window import NewLutWindow

class NewImageWindow(Toplevel):
    def __init__(self, master = None, pathToImage = None, name=None): 
        super().__init__(master = master)

        self.set_basic(master, pathToImage, name)
        self.set_images(pathToImage)
        self.set_geometry()
        self.place_menu()
        self.bind_functions()

    @staticmethod
    def duplicate_window(master, pathToImage,  name):
        NewImageWindow(master, pathToImage, name)

    def resize_img(self, event):
        new_width = event.width
        new_height = event.height

        self.imageFromArray = self.imageCopy.resize((new_width, new_height))
        self.photoImage = ImageTk.PhotoImage(self.imageFromArray)
        self.imagePanel.configure(image = self.photoImage)

    def set_geometry(self):
        self.geometry('{}x{}'.format(self.imageFromArray.width, self.imageFromArray.height))
        self.minsize(200, 200)

    def place_menu(self):
        self.top_menu = tk.Menu()
        self.top_menu.add_command(label='LUT', compound=tk.LEFT, command= lambda: NewLutWindow(self.image, self.name, self))
        self.top_menu.add_command(label='Histogram', compound=tk.LEFT, command= lambda: NewHistogramWindow(self.image, self.name, self))
        self.top_menu.add_command(label='Linia profilu', compound=tk.LEFT)
        self.top_menu.add_command(label='Linia profilu', compound=tk.LEFT)
        self.config(menu = self.top_menu)

    def bind_functions(self):
        self.bind('<Configure>', self.resize_img)
        self.bind('<Control-d>', lambda event: NewImageWindow.duplicate_window(self.master, self.path, self.name + '(Kopia)'))

    def set_images(self, pathToImage):
        self.image = ImageSaved(pathToImage)
        self.imageFromArray = Image.fromarray(self.image.cv2Image)
        self.imageCopy = self.imageFromArray.copy()

    def set_basic(self, master, pathToImage, name):
        self.master = master
        self.path = pathToImage
        self.name = name 
        self.title(name) 
        self.imagePanel = tk.Label(self)
        self.imagePanel.place(relwidth=1, relheight = 1, x=0, y=0)