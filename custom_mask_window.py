import copy
from tkinter import Entry, StringVar, Toplevel
from tkinter.ttk import Button
from icons_import import saveIcon, closeIcon

class NewCustomMaskWindow(Toplevel):
    def __init__(self, master = None, borderPixels=None): 
        super().__init__(master = master)   
        self.borderPixels = borderPixels
        self.set_basic()
        self.set_widgets()         

        
    def set_basic(self):
        self.minsize(300, 300)
        self.maxsize(300, 300)
        self.title("Operacje sąsiedztwa")

    def set_widgets(self):
        self.maskVar = [StringVar(self) for _ in range(49)]
        self.maskEntries = [Entry(self, textvariable=self.maskVar[i], justify='center', font=("Helvetica", 15)) for i in range(49)]

        self.saveButton = Button(self, image=saveIcon, command=self.update_image)
        self.cancelButton = Button(self, image=closeIcon, command=self.cancel)

        self.place_widgets()

    def update_image(self):
        self.cancel()

    def place_widgets(self):
        for i in range(3):
            for j in range(3):
                self.maskEntries[i*3+j].place(width=80, height=80, x=j*80+30, y=i*80+5)
                self.maskVar[i*3+j].set(0)


        self.saveButton.place(width=40, height=40, x=125, y=255)
        self.cancelButton.place(width=40, height=40, x=225, y=255)

    def cancel(self):
        self.master.image.cv2Image = copy.deepcopy(self.master.image.copy)
        self.master.update_visible_image()
        self.master.image.fill_histogram()
        self.master.update_child_windows()
        self.master.thresholdScaleWindow = None
        self.destroy()   
        