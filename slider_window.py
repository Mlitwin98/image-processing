from tkinter import Scale, Toplevel, IntVar, Checkbutton
from tkinter import ttk
from tkinter.constants import VERTICAL

class NewSliderWindow(Toplevel):
    def __init__(self, name, master = None): 
            super().__init__(master = master)
            self.set_basic(name)

            
    def set_basic(self, name):
        self.overrideredirect(1)

        parentX = self.master.winfo_rootx()
        parentY = self.master.winfo_rooty()
        parentHeight = self.master.winfo_height()
        parentWidth = self.master.winfo_width()
        self.geometry('%dx%d+%d+%d' % (50, parentHeight, parentX+parentWidth+2, parentY))

        self.set_scale(parentHeight)
        self.set_checkButton(parentHeight)
        
        self.title("Progowanie {}".format(name))

    def set_scale(self, parentHeight):
        self.var = IntVar()
        self.scale = Scale(self, length=256, from_=0, to=255, orient=VERTICAL, command=lambda e:self.update_image(int(self.var.get()), self.cbVal.get()), variable=self.var, digits=1, resolution=1)
        self.scale.place(relx=-0.1, rely=0, relwidth=0.9, relheight=0.9)
        self.scale.set(0)

    def set_checkButton(self, parentHeight):
        self.cbVal = IntVar()
        self.cb = ttk.Checkbutton(self, width=0, variable=self.cbVal, command=lambda:self.update_image(int(self.var.get()), self.cbVal.get()))
        self.cb.place(relx=0.4, rely=0.9)
        self.cb.invoke()

    def update_image(self, thresholdVal, checkBoxVal):
        self.master.image.threshold(thresholdVal, checkBoxVal)
        self.master.update_visible_image()
        self.master.update_child_windows()