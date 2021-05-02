import copy
from tkinter import StringVar, Toplevel, messagebox ,Spinbox
from tkinter.ttk import Button

from numpy import int64
from numpy.core.fromnumeric import reshape, sum, all
from icons_import import saveIcon, closeIcon

class NewCustomMaskWindow(Toplevel):
    def __init__(self, master=None): 
        super().__init__(master = master)
        self.set_basic()
        self.set_widgets()         

        
    def set_basic(self):
        self.minsize(300, 300)
        self.maxsize(300, 300)
        self.title("Własna maska")
        self.protocol("WM_DELETE_WINDOW", lambda: self.cancel())

    def set_widgets(self):
        self.maskVar = [StringVar(self, value="0") for _ in range(9)]
        self.maskEntries = [Spinbox(self, justify='center', font=("Helvetica", 15), from_=-9999, to=9999, textvariable=self.maskVar[i], command=self.update_preview, state='readonly') for i in range(9)]

        self.saveButton = Button(self, image=saveIcon, command=self.update_image)
        self.cancelButton = Button(self, image=closeIcon, command=self.cancel)

        self.place_widgets()

    def update_image(self):
        mask = self.getMask()
        if mask is None:
            messagebox.showerror("Błąd", "Wprowadź poprawą maskę")
            self.lift()
            self.focus_set()
            return
        else:
            self.master.image.cv2Image = copy.deepcopy(self.master.image.copy)
            self.master.image.neighborOperations("CUSTOM", self.master.border.get(), mask)
            self.master.image.copy = copy.deepcopy(self.master.image.cv2Image)
            self.master.update_visible_image()
            self.master.update_child_windows()
            self.destroy()

    def update_preview(self):
        mask = self.getMask()
        if mask is None:
            return
        else:
            self.master.image.cv2Image = copy.deepcopy(self.master.image.copy)
            self.master.image.neighborOperations("CUSTOM", self.master.border.get(), mask)
            self.master.update_visible_image()
            self.master.update_child_windows()

    def place_widgets(self):
        for i in range(3):
            for j in range(3):
                self.maskEntries[i*3+j].place(width=80, height=80, x=j*80+30, y=i*80+5)


        self.saveButton.place(width=40, height=40, x=70, y=255)
        self.cancelButton.place(width=40, height=40, x=190, y=255)

    def cancel(self):
        self.master.image.cv2Image = copy.deepcopy(self.master.image.copy)
        self.master.update_visible_image()
        self.master.image.fill_histogram()
        self.master.update_child_windows()
        self.destroy()   
        
    def getMask(self):
        try:
            values = [int(val.get()) for val in self.maskVar]
        except ValueError: #AKTUALNIE NIE POTRZEBNE BO POLA SĄ READONLY
            return None

        mask = reshape(values, (3,3))
        if all(mask==0):
            return None
        else:
            if sum(mask) != 0:
                mask = int64(mask)/sum(mask)

            return mask