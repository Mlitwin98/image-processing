from tkinter import Label, StringVar, Toplevel, messagebox ,Spinbox
from tkinter.ttk import Button

import numpy as np
from icons_import import saveIcon, closeIcon

class NewCustomStretchWindow(Toplevel):
    def __init__(self, master=None): 
        super().__init__(master = master)
        self.set_basic()
        self.set_widgets()         

        
    def set_basic(self):
        self.minsize(300, 200)
        self.maxsize(300, 200)
        self.title("Rozciąganie")
        self.protocol("WM_DELETE_WINDOW", lambda: self.cancel())

    def set_widgets(self):
        self.p1 = StringVar(self, value=np.amin(self.master.image.cv2Image))
        self.p2 = StringVar(self, value=np.amax(self.master.image.cv2Image))
        self.q1 = StringVar(self, value="0")
        self.q2 = StringVar(self, value="255")

        self.p1Entry = Spinbox(self, justify='center', font=("Helvetica", 15), from_=0, to=255, textvariable=self.p1)
        self.p2Entry = Spinbox(self, justify='center', font=("Helvetica", 15), from_=0, to=255, textvariable=self.p2)
        self.q1Entry = Spinbox(self, justify='center', font=("Helvetica", 15), from_=0, to=255, textvariable=self.q1)
        self.q2Entry = Spinbox(self, justify='center', font=("Helvetica", 15), from_=0, to=255, textvariable=self.q2)

        self.saveButton = Button(self, image=saveIcon, command=self.update_image)
        self.cancelButton = Button(self, image=closeIcon, command=self.cancel)

        self.place_widgets()

    def update_image(self):
        p1, p2, q1, q2 = self.getValues()
        if p1 is None:
            messagebox.showerror("Błąd", "Wprowadź poprawne przedziały w postaci liczb całkowitych <0;255>")
            self.lift()
            self.focus_set()
            return
        else:
            self.master.image.stretch(p1, p2, q1, q2)
            self.master.manager.new_state(self.master.image.cv2Image)
            self.master.update_visible_image()
            self.master.update_child_windows()
            self.destroy()

    def place_widgets(self):
        Label(self, text="p1: ", font=("Helvetica", 15)).place(x=10, y=20)
        Label(self, text="p2: ", font=("Helvetica", 15)).place(x=130, y=20)
        Label(self, text="q1: ", font=("Helvetica", 15)).place(x=10, y=105)
        Label(self, text="q2: ", font=("Helvetica", 15)).place(x=130, y=105)
        self.p1Entry.place(width=80, height=50, x=50, y=10)
        self.p2Entry.place(width=80, height=50, x=170, y=10)
        self.q1Entry.place(width=80, height=50, x=50, y=90)
        self.q2Entry.place(width=80, height=50, x=170, y=90)


        self.saveButton.place(width=40, height=40, x=70, y=155)
        self.cancelButton.place(width=40, height=40, x=190, y=155)

    def cancel(self):
        self.destroy()   
        
    def getValues(self):
        try:
            values = [int(val.get()) for val in [self.p1, self.p2, self.q1, self.q2]]
        except ValueError:
            return None

        return values[0], values[1], values[2], values[3]