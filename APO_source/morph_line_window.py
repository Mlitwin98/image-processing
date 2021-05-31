import copy
from tkinter import Checkbutton, IntVar, Label, StringVar, Toplevel ,Spinbox
from tkinter.ttk import Button, OptionMenu

from icons_import import saveIcon, closeIcon

class NewMorphLineWindow(Toplevel):
    def __init__(self, master=None): 
        super().__init__(master = master)
        self.set_basic()
        self.set_widgets()         

        
    def set_basic(self):
        self.minsize(600, 400)
        self.maxsize(600, 400)
        self.title("Ekstrakcja linii")
        self.protocol("WM_DELETE_WINDOW", lambda: self.cancel())

        self.handleBorder = {
            "Bez zmian (isolated)":0, 
            "Odbicie lustrzane (reflect)":1, 
            "Powielenie skrajnego piksela (replicate)":2
        }

    def set_widgets(self):
        self.horizontalSizeW = StringVar(self, value="3")
        self.horizontalSizeH = StringVar(self, value="1")
        self.verticalSizeW = StringVar(self, value="3")
        self.verticalSizeH = StringVar(self, value="1")
        self.borderType = StringVar(self, list(self.handleBorder.keys())[0])
        self.cbVarHorizontal = IntVar(value=1)
        self.cbVarVertical = IntVar(value=1)
        self.cbVarOuter = IntVar(value=1)
        self.cbVarNegate = IntVar(value=0)

        self.sizeHorizontalWSpin = Spinbox(self, justify='center', font=("Helvetica", 15), from_=1, to=9999, textvariable=self.horizontalSizeW, command=self.update_preview, state='readonly', increment=2)
        self.sizeHorizontalHSpin = Spinbox(self, justify='center', font=("Helvetica", 15), from_=1, to=9999, textvariable=self.horizontalSizeH, command=self.update_preview, state='readonly', increment=2)
        self.sizeVerticalWSpin = Spinbox(self, justify='center', font=("Helvetica", 15), from_=1, to=9999, textvariable=self.verticalSizeW, command=self.update_preview, state='readonly', increment=2)
        self.sizeVerticalHSpin = Spinbox(self, justify='center', font=("Helvetica", 15), from_=1, to=9999, textvariable=self.verticalSizeH, command=self.update_preview, state='readonly', increment=2)

        self.horizontalSizeW.trace("w", self.update_preview)
        self.horizontalSizeH.trace("w", self.update_preview)
        self.verticalSizeW.trace("w", self.update_preview)
        self.verticalSizeH.trace("w", self.update_preview)
        self.borderType.trace("w", self.update_preview)
        self.cbVarHorizontal.trace("w", self.update_preview)
        self.cbVarVertical.trace("w", self.update_preview)
        self.cbVarOuter.trace("w", self.update_preview)
        self.cbVarNegate.trace("w", self.update_preview)
        
        self.cbHorizontal = Checkbutton(self, width=0, variable=self.cbVarHorizontal)
        self.cbVertical = Checkbutton(self, width=0, variable=self.cbVarVertical)
        self.cbOuterOnly = Checkbutton(self, width=0, variable=self.cbVarOuter)
        self.cbNegateFirst = Checkbutton(self, width=0, variable=self.cbVarNegate)

        self.borderList = OptionMenu(self, self.borderType)

        for border in self.handleBorder:
            self.borderList['menu'].add_command(label=border, command=lambda v=border: self.borderType.set(v))


        self.saveButton = Button(self, image=saveIcon, command=self.update_image)
        self.cancelButton = Button(self, image=closeIcon, command=self.cancel)

        self.update_preview()
        self.place_widgets()

    def update_image(self):
        self.master.image.cv2Image = copy.deepcopy(self.master.image.copy)
        self.master.image.morph_line(int(self.horizontalSizeW.get()), int(self.horizontalSizeH.get()), int(self.verticalSizeW.get()), int(self.verticalSizeH.get()), self.cbVarHorizontal.get(), self.cbVarVertical.get(), self.handleBorder[self.borderType.get()], self.cbVarOuter.get(), self.cbVarNegate.get())
        self.master.image.copy = copy.deepcopy(self.master.image.cv2Image)
        self.master.manager.new_state(self.master.image.cv2Image)
        self.master.update_visible_image()
        self.master.update_child_windows()
        self.destroy()

    def update_preview(self, *args):
        self.sizeHorizontalWSpin.config(from_=int(self.horizontalSizeH.get())+2)
        self.sizeHorizontalHSpin.config(to=int(self.horizontalSizeW.get())-2)
        self.sizeVerticalWSpin.config(from_=int(self.verticalSizeH.get())+2)
        self.sizeVerticalHSpin.config(to=int(self.verticalSizeW.get())-2)
        self.master.image.cv2Image = copy.deepcopy(self.master.image.copy)
        self.master.image.morph_line(int(self.horizontalSizeW.get()), int(self.horizontalSizeH.get()), int(self.verticalSizeW.get()), int(self.verticalSizeH.get()), self.cbVarHorizontal.get(), self.cbVarVertical.get(), self.handleBorder[self.borderType.get()], self.cbVarOuter.get(), self.cbVarNegate.get())
        self.master.update_visible_image()
        self.master.update_child_windows()

    def place_widgets(self):
        Label(self, text="Poziome linie", font=("Helvetica", 15)).place(x=85, y=15)
        Label(self, text="Pionowe linie", font=("Helvetica", 15)).place(x=395, y=15)

        self.sizeHorizontalWSpin.place(width=100, height=50, x=150, y=60)
        self.sizeHorizontalHSpin.place(width=100, height=50, x=150, y=120)
        self.sizeVerticalWSpin.place(width=100, height=50, x=450, y=60)
        self.sizeVerticalHSpin.place(width=100, height=50, x=450, y=120)

        Label(self, text="Min. długość", font=("Helvetica", 15)).place(x=30, y=70)
        Label(self, text="Min. grubość", font=("Helvetica", 15)).place(x=30, y=130)
        Label(self, text="Min. długość", font=("Helvetica", 15)).place(x=330, y=70)
        Label(self, text="Min. grubość", font=("Helvetica", 15)).place(x=330, y=130)

        Label(self, text="Szukać poziomych?", font=("Helvetica", 9)).place(x=70, y=175)
        Label(self, text="Szukać pionowych?", font=("Helvetica", 9)).place(x=380, y=175)

        self.cbHorizontal.place(x=180, y=175)
        self.cbVertical.place(x=500, y=175)

        Label(self, text="Szukać tylko zewnętrznych?", font=("Helvetica", 11)).place(x=190, y=225)
        Label(self, text="Wstępnie zanegować?", font=("Helvetica", 11)).place(x=190, y=255)
        self.cbOuterOnly.place(x=390, y=225)
        self.cbNegateFirst.place(x=390, y=255)
        self.borderList.place(width=200, height=50, x=200, y=300)

        self.saveButton.place(width=40, height=40, x=220, y=355)
        self.cancelButton.place(width=40, height=40, x=340, y=355)

    def cancel(self):
        self.master.image.cv2Image = copy.deepcopy(self.master.image.copy)
        self.master.update_visible_image()
        self.master.image.fill_histogram()
        self.master.update_child_windows()
        self.destroy()