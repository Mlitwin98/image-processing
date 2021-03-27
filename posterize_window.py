from tkinter import Spinbox, Toplevel
from tkinter.constants import RIGHT

class NewPosterizeWindow(Toplevel):
    def __init__(self, name, master = None): 
            super().__init__(master = master)
            self.set_basic(name)

            self.master.image.posterize(2)

    def set_basic(self, name):
        self.overrideredirect(1)

        parentX = self.master.winfo_rootx()
        parentY = self.master.winfo_rooty()
        parentHeight = self.master.winfo_height()
        parentWidth = self.master.winfo_width()
        self.geometry('%dx%d+%d+%d' % (parentWidth/2, 30, parentX, parentY+parentHeight))

        
        self.spinBox = Spinbox(self, command=lambda:self.update_image(), from_=2, to=255, width=3, font=("Helvetica", 15), justify=RIGHT)
        self.spinBox.pack()
        self.spinBox.delete(0,"end")
        self.spinBox.insert(0,2)

        
        self.title("Redukcja poziomów szarości {}".format(name))


    def update_image(self):
        self.master.image.posterize(int(self.spinBox.get()))
        self.master.update_visible_image()
        self.master.update_child_windows()