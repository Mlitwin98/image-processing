from os import access
from tkinter import Spinbox, Toplevel, PhotoImage, Button
from tkinter.constants import LEFT, RIGHT, SE, SW

class NewPosterizeWindow(Toplevel):
    def __init__(self, name, master = None): 
            super().__init__(master = master)
            self.set_basic(name)

            self.master.image.posterize(2)

            self.bind('<Configure>', lambda e: self.place_buttons())

    def set_basic(self, name):
        self.overrideredirect(1)
        self.set_geometry()        
        self.set_spinbox()
        self.set_save_closeButtons()       
        self.title("Redukcja poziomów szarości {}".format(name))

    def set_geometry(self):
        self.height = 30
        parentX = self.master.winfo_rootx()
        parentY = self.master.winfo_rooty()
        parentHeight = self.master.winfo_height()
        parentWidth = self.master.winfo_width()
        self.geometry('%dx%d+%d+%d' % (parentWidth, self.height, parentX, parentY+parentHeight+2))

    def set_spinbox(self):
        self.spinBox = Spinbox(self, command=lambda:self.update_preview(), from_=2, to=255, width=3, font=("Helvetica", 15), justify=LEFT)
        self.spinBox.place(relx=0.375, relwidth=0.25)
        self.spinBox.delete(0,"end")
        self.spinBox.insert(0,2)

    def set_save_closeButtons(self):
        self.saveIcon = PhotoImage(file=r"icons/tick.png")
        self.closeIcon = PhotoImage(file=r"icons/close.png")
        self.saveButton = Button(self, image=self.saveIcon, command=lambda: self.update_image())
        self.cancelButton = Button(self, image=self.closeIcon, command=lambda: self.cancel())
        self.saveButton.place(relx=1-((2*self.height)/self.master.winfo_width()), relheight=1)
        self.cancelButton.place(relx=1-(self.height/self.master.winfo_width()), relheight=1)

    def place_buttons(self):
        self.saveButton.place(relx=1-((2*self.height)/self.master.winfo_width()), relheight=1, width=self.height)
        self.cancelButton.place(relx=1-(self.height/self.master.winfo_width()), relheight=1, width=self.height)

    def update_preview(self):
        self.master.image.posterize(int(self.spinBox.get()))
        self.master.update_visible_image()

    def update_image(self):
        self.master.image.fill_histogram()
        self.master.update_child_windows()

    def cancel(self):
        self.master.image.cv2Image = self.master.image.copy
        self.master.update_visible_image()
        self.master.image.fill_histogram()
        self.master.update_child_windows()
        self.master.posterizeWindow = None
        self.destroy()