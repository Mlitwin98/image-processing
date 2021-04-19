import copy
from tkinter import Toplevel, Button
from tkinter.constants import GROOVE

import cv2

class NewPixelAsker(Toplevel):
    def __init__(self, master = None, operation=None): 
        super().__init__(master = master)   

        self.operation = operation
        self.set_basic()
        self.set_widgets()         

        
    def set_basic(self):
        self.minsize(300, 300)
        self.maxsize(300, 300)
        self.title("Skrajne pixele")

    def set_widgets(self):
        self.isolatedButton = Button(self, text="Bez zmian(isolated)", font=("Helvetica", 15), command=lambda:self.click(cv2.BORDER_ISOLATED), relief=GROOVE)
        self.reflectButton = Button(self, text="Odbicie lustrzane(reflect)", font=("Helvetica", 15), command=lambda:self.click(cv2.BORDER_REFLECT), relief=GROOVE)
        self.replicateButton = Button(self, text="Powielenie skrajnego(replicate)", font=("Helvetica", 15), command=lambda:self.click(cv2.BORDER_REPLICATE), relief=GROOVE)

        self.place_widgets()


    def place_widgets(self):
        self.isolatedButton.place(width=290, height=90, x=5, y=0)
        self.reflectButton.place(width=290, height=90, x=5, y=100)
        self.replicateButton.place(width=290, height=90, x=5, y=200)
        
    def click(self, borderOption):
        self.master.image.neighborOperations(self.operation, borderOption)
        self.master.image.copy = copy.deepcopy(self.master.image.cv2Image)
        self.master.update_visible_image()
        self.master.update_child_windows()
        self.destroy()