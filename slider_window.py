from tkinter import Scale, Toplevel, IntVar, Checkbutton
from tkinter.constants import HORIZONTAL

class NewSliderWindow(Toplevel):
    def __init__(self, name, master = None): 
            super().__init__(master = master)
            self.set_basic(name)

            self.scale.set(0)
            self.master.image.threshold(0, False)

    def set_basic(self, name):
        if self.master.image.isGrayScale:
            self.geometry('300x80')
            self.minsize(300, 80)
        else:
            self.geometry('400x200')
            self.minsize(300, 200)

        self.var = IntVar()
        self.scale = Scale(self, length=256, from_=0, to=255, orient=HORIZONTAL, command=lambda e:self.update_image(int(self.var.get()), self.cbVal.get()), variable=self.var, digits=1, resolution=1)
        self.scale.pack()

        self.cbVal = IntVar()
        self.cb = Checkbutton(self, text='Zachowaj wartość', variable=self.cbVal, command=lambda:self.update_image(int(self.var.get()), self.cbVal.get()))
        self.cb.pack()

        self.maxsize(200, 100)
        self.title("Progowanie {}".format(name))


    def update_image(self, thresholdVal, checkBoxVal):
        self.master.image.threshold(thresholdVal, checkBoxVal)
        self.master.update_visible_image()
        self.master.update_child_windows()