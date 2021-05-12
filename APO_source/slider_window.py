import copy
from tkinter import Scale, Toplevel, IntVar
from tkinter.constants import VERTICAL
from tkinter.ttk import Button, Checkbutton
from icons_import import saveIcon, closeIcon

class NewSliderWindow(Toplevel):
    def __init__(self, master = None): 
            super().__init__(master = master)
            self.set_basic()

            self.bind('<Configure>', lambda e: self.place_buttons())
       
    def set_basic(self):
        self.overrideredirect(1)
        self.set_geometry()
        self.set_scale()
        self.set_checkButton()
        self.set_save_closeButtons()

    def set_geometry(self):
        self.width = 60
        parentX = self.master.winfo_rootx()
        parentY = self.master.winfo_rooty()
        parentHeight = self.master.winfo_height()
        parentWidth = self.master.winfo_width()
        self.geometry('%dx%d+%d+%d' % (self.width, parentHeight, parentX+parentWidth+2, parentY))

    def set_save_closeButtons(self):
        self.saveButton = Button(self, image=saveIcon, command=self.update_image)
        self.cancelButton = Button(self, image=closeIcon, command=self.cancel)

        self.saveButton.place(relx=0.1, rely=0.8, relwidth=0.4)
        self.cancelButton.place(relx=0.55, rely=0.8, relwidth=0.4)

        self.saveButton.place(relx=0.1, rely=1-((0.4*self.width)/self.master.winfo_height()), relwidth=0.4)
        self.cancelButton.place(relx=0.55, rely=1-((0.4*self.width)/self.master.winfo_height()), relwidth=0.4)

    def place_buttons(self):
        self.saveButton.place(relx=0.03, rely=1-((0.45*self.width)/self.master.winfo_height()), relwidth=0.45)
        self.cancelButton.place(relx=0.52, rely=1-((0.45*self.width)/self.master.winfo_height()), relwidth=0.45)

    def set_scale(self):
        self.var = IntVar()
        self.scale = Scale(self, length=256, from_=0, to=255, orient=VERTICAL, command=lambda e:self.update_preview(int(self.var.get()), self.cbVal.get()), variable=self.var, digits=1, resolution=1)
        self.scale.place(relx=0, rely=0.1, relwidth=0.9, relheight=0.7)
        self.scale.set(0)

    def set_checkButton(self):
        self.cbVal = IntVar()
        self.cb = Checkbutton(self, width=0, variable=self.cbVal, command=lambda:self.update_preview(int(self.var.get()), self.cbVal.get()))
        self.cb.place(relx=0.4, rely=0.78)
        self.cb.invoke()

    #UPDATE IMAGE ON SLIDER CHANGE
    def update_preview(self, thresholdVal, checkBoxVal):
        self.master.image.threshold(thresholdVal, checkBoxVal)
        self.master.update_visible_image()
        
    #UPDATE IMAGE ON "SAVE" AND UPDATE HISTOGRAM
    def update_image(self):
        self.master.update_visible_image()
        self.master.image.fill_histogram()
        self.master.update_child_windows()
        self.master.thresholdScaleWindow = None
        self.destroy()

    #GO BACK TO ORIGINAL ON "CANCEL"
    def cancel(self):
        self.master.image.cv2Image = copy.deepcopy(self.master.image.copy)
        self.master.update_visible_image()
        self.master.image.fill_histogram()
        self.master.update_child_windows()
        self.master.thresholdScaleWindow = None
        self.destroy()

class NewAdaptiveSliderWindow(NewSliderWindow):
    def set_basic(self):
        self.overrideredirect(1)
        self.set_geometry()
        self.set_scale()
        self.set_save_closeButtons()

    def fix(self, n):
        n = int(n)
        if not n % 2:
            self.scale.set(n+1 if n > self.past else n-1)
            self.update_preview(int(self.var.get()))
            self.past = self.scale.get()
        if n%2:
            self.update_preview(int(self.var.get()))

    def set_scale(self):
        self.var = IntVar()
        self.scale = Scale(self, length=300, from_=3, to=255, orient=VERTICAL, command=self.fix, variable=self.var, digits=1)
        self.update_preview(int(self.var.get()))
        self.scale.place(relx=0, rely=0.1, relwidth=0.9, relheight=0.7)
        self.scale.set(0)

    def update_preview(self, windowSize):
        self.master.image.threshold_adapt(windowSize)
        self.master.update_visible_image()

    def __init__(self, master = None): 
        self.past = 3
        super().__init__(master)
