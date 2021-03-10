import cv2
import tkinter as tk
from tkinter import PhotoImage, Toplevel
from PIL import Image, ImageTk
import numpy as np

class ImageSaved():
    def __init__(self, path):
        self.cv2Image = cv2.imread(path, 1)
        self.isGrayScale = self.isgray()
        if self.isGrayScale:
            self.cv2Image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            self.lut = [0]*256
        else:
            self.cv2Image = cv2.imread(path, cv2.IMREAD_COLOR)
            self.cv2Image = cv2.cvtColor(self.cv2Image, cv2.COLOR_BGR2RGB)
            self.lut = np.zeros(shape=(256, 3))

        self.name = path
        self.size = self.cv2Image.size
        self.fill_lut()

    def isgray(self):
        b,g,r = self.cv2Image[:,:,0], self.cv2Image[:,:,1], self.cv2Image[:,:,2]
        if (b==g).all() and (b==r).all(): return True
        return False

    def fill_lut(self):
        if self.isGrayScale:
            h, w = self.cv2Image.shape
            for i in range(w):
                for j in range(h):
                    self.lut[self.cv2Image[i][j]] += 1
        else:
            h, w, c = self.cv2Image.shape
            for i in range(w):
                for j in range(h):
                    for k in range(c):
                        self.lut[self.cv2Image[i][j][k], k] += 1        

        
class NewImageWindow(Toplevel):
    def __init__(self, master = None, pathToImage = None, name=None): 
        super().__init__(master = master)
        self.master = master
        self.path = pathToImage
        self.name = name 
        self.title(name) 
        self.minsize()

        self.image = ImageSaved(pathToImage)

        self.imageFromArray = Image.fromarray(self.image.cv2Image)
        self.imageCopy = self.imageFromArray.copy()
        self.photoImage = ImageTk.PhotoImage(self.imageFromArray)

        self.imagePanel = tk.Label(self, image=self.photoImage)
        self.imagePanel.image = self.photoImage
        self.imagePanel.place(relwidth = 0.9, relheight = 1, x=0, y=0)

        self.showHistogramBtn = tk.Button(self, text="Histogram")
        self.showHistogramBtn.place(width=50, height = 50, relx= 0.95, anchor=tk.NE)

        self.showLutBtn = tk.Button(self, text="LUT")
        self.showLutBtn.place(width=50, height = 50, anchor=tk.NE, relx= 0.95,  y = 50)

        self.bind('<Configure>', self.resize_img)
        self.bind('<Control-d>', lambda event: NewImageWindow.duplicate_window(self.master, self.path, self.name + '(Kopia)'))

    @staticmethod
    def duplicate_window(master, pathToImage,  name):
        NewImageWindow(master, pathToImage, name)

    def resize_img(self, event):
        new_width = event.width
        new_height = event.height

        self.imageFromArray = self.imageCopy.resize((new_width, new_height))
        
        self.photoImage = ImageTk.PhotoImage(self.imageFromArray)
        self.imagePanel.configure(image=self.photoImage)