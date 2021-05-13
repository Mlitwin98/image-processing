import copy
from tkinter import StringVar, Toplevel, messagebox ,Spinbox
from tkinter.ttk import Button
from scipy.signal import convolve2d as conv2
from numpy import int64
from numpy.core.fromnumeric import reshape, sum, all
from icons_import import saveIcon, closeIcon

class NewCustomMaskWindow(Toplevel):
    def __init__(self, master=None): 
        super().__init__(master = master)
        self.set_basic(300, 300)
        self.set_widgets()         

        
    def set_basic(self, width, height):
        self.minsize(width, height)
        self.maxsize(width, height)
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
            self.master.image.neighbor_operations("CUSTOM", self.master.border.get(), mask)
            self.master.image.copy = copy.deepcopy(self.master.image.cv2Image)
            self.master.manager.new_state(self.master.image.cv2Image)
            self.master.update_visible_image()
            self.master.update_child_windows()
            self.destroy()

    def update_preview(self):
        mask = self.getMask()
        if mask is None:
            return
        else:
            self.master.image.cv2Image = copy.deepcopy(self.master.image.copy)
            self.master.image.neighbor_operations("CUSTOM", self.master.border.get(), mask)
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


class NewCustomMaskWindowConv(NewCustomMaskWindow):
    def __init__(self, master=None): 
        super().__init__(master = master)
        super().set_basic(400, 470)
        self.set_widgets()         


    def set_widgets(self):
        self.mask1Var = [StringVar(self, value="0") for _ in range(9)]
        self.mask2Var = [StringVar(self, value="0") for _ in range(9)]
        self.outputMaskVar = [StringVar(self, value="0") for _ in range(25)]

        self.mask1Entries = [Spinbox(self, justify='center', font=("Helvetica", 15), from_=-9999, to=9999, textvariable=self.mask1Var[i], command=self.update_preview, state='readonly') for i in range(9)]
        self.mask2Entries = [Spinbox(self, justify='center', font=("Helvetica", 15), from_=-9999, to=9999, textvariable=self.mask2Var[i], command=self.update_preview, state='readonly') for i in range(9)]
        self.outputMaskEntries = [Spinbox(self, justify='center', font=("Helvetica", 15), from_=-9999, to=9999, textvariable=self.outputMaskVar[i], state='disabled') for i in range(25)]
       
        self.saveButton = Button(self, image=saveIcon, command=self.update_image)
        self.cancelButton = Button(self, image=closeIcon, command=super().cancel)

        self.place_widgets()

    def update_image(self):
        mask1 = self.getMask(self.mask1Var)
        mask2 = self.getMask(self.mask2Var)
        if mask1 is None or mask2 is None:
            messagebox.showerror("Błąd", "Wprowadź poprawne maski")
            self.lift()
            self.focus_set()
            return
        else:
            mask = conv2(mask1, mask2, mode='full')
            self.master.image.cv2Image = copy.deepcopy(self.master.image.copy)
            self.master.image.neighbor_operations("CUSTOM", self.master.border.get(), mask)
            self.master.image.copy = copy.deepcopy(self.master.image.cv2Image)
            self.master.manager.new_state(self.master.image.cv2Image)
            self.master.update_visible_image()
            self.master.update_child_windows()
            self.destroy()

    def update_preview(self):
        mask1 = self.getMask(self.mask1Var)
        mask2 = self.getMask(self.mask2Var)
        if mask1 is None or mask2 is None:
            return
        else:
            mask = conv2(mask1, mask2, mode='full')
            for i in range(5):
                for j in range(5):
                    self.outputMaskVar[i*5+j].set(mask[i,j])
            self.master.image.cv2Image = copy.deepcopy(self.master.image.copy)
            self.master.image.neighbor_operations("CUSTOM", self.master.border.get(), mask)
            self.master.update_visible_image()
            self.master.update_child_windows()

    def place_widgets(self):
        for i in range(3):
            for j in range(3):
                self.mask1Entries[i*3+j].place(width=50, height=50, x=j*50+20, y=i*50+5)
                self.mask2Entries[i*3+j].place(width=50, height=50, x=j*50+230, y=i*50+5)

        for i in range(5):
            for j in range(5):
                self.outputMaskEntries[i*5+j].place(width=50, height=50, x=j*50+75, y=i*50+170)

        self.saveButton.place(width=40, height=40, x=120, y=425)
        self.cancelButton.place(width=40, height=40, x=240, y=425)

    def getMask(self, varList):
        try:
            values = [int(val.get()) for val in varList]
        except ValueError: #AKTUALNIE NIE POTRZEBNE BO POLA SĄ READONLY
            return None

        mask = reshape(values, (3,3))
        if all(mask==0):
            return None
        else:
            return mask