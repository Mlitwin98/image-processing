import copy
from tkinter import StringVar, Toplevel ,Spinbox
from tkinter.ttk import Button, OptionMenu

from icons_import import saveIcon, closeIcon

class NewMorphWindow(Toplevel):
    def __init__(self, master=None): 
        super().__init__(master = master)
        self.set_basic()
        self.set_widgets()         

        
    def set_basic(self):
        self.minsize(300, 300)
        self.maxsize(300, 300)
        self.title("Operacje morfologiczne")
        self.protocol("WM_DELETE_WINDOW", lambda: self.cancel())

        self.operations = ["EROZJA", "DYLACJA", "OTWARCIE", "ZAMKNIĘCIE",]
        self.shapes = ["KWADRAT", "ROMB"]
        self.handleBorder = {
            "Bez zmian (isolated)":0, 
            "Odbicie lustrzane (reflect)":1, 
            "Powielenie skrajnego piksela (replicate)":2
        }

    def set_widgets(self):
        self.operationChoice = StringVar(self, self.operations[0])
        self.shape = StringVar(self, value=self.shapes[0])
        self.size = StringVar(self, value="3")
        self.borderType = StringVar(self, list(self.handleBorder.keys())[0])


        self.operationChoice.trace("w", self.update_preview)
        self.shape.trace("w", self.update_preview)
        self.borderType.trace("w", self.update_preview)

        

        self.operationList = OptionMenu(self, self.operationChoice)
        self.shapeList = OptionMenu(self, self.shape)
        self.sizeSpin = Spinbox(self, justify='center', font=("Helvetica", 15), from_=3, to=9999, textvariable=self.size, command=self.update_preview, state='readonly', increment=2)
        self.borderList = OptionMenu(self, self.borderType)

        for oper in self.operations:
            self.operationList['menu'].add_command(label=oper, command=lambda v=oper: self.operationChoice.set(v))

        for sh in self.shapes:
            self.shapeList['menu'].add_command(label=sh, command=lambda v=sh: self.shape.set(v))

        for border in self.handleBorder:
            self.borderList['menu'].add_command(label=border, command=lambda v=border: self.borderType.set(v))


        self.saveButton = Button(self, image=saveIcon, command=self.update_image)
        self.cancelButton = Button(self, image=closeIcon, command=self.cancel)

        self.update_preview()
        self.place_widgets()

    #POPRAW
    def update_image(self):
        self.master.image.cv2Image = copy.deepcopy(self.master.image.copy)
        self.master.image.morphOperations(self.operationChoice.get(), self.shape.get(), int(self.size.get()), self.handleBorder[self.borderType.get()])
        self.master.image.copy = copy.deepcopy(self.master.image.cv2Image)
        self.master.update_visible_image()
        self.master.update_child_windows()
        self.destroy()

    def update_preview(self, *args):
        self.master.image.cv2Image = copy.deepcopy(self.master.image.copy)
        self.master.image.morphOperations(self.operationChoice.get(), self.shape.get(), int(self.size.get()), self.handleBorder[self.borderType.get()])
        self.master.update_visible_image()
        self.master.update_child_windows()

    def place_widgets(self):
        self.operationList.place(width=250, height=50, x=25, y=20)
        self.shapeList.place(width=100, height=50, x=25, y=80)
        self.sizeSpin.place(width=100, height=50, x=175, y=80)
        self.borderList.place(width=250, height=50, x=25, y=140)


        self.saveButton.place(width=40, height=40, x=70, y=255)
        self.cancelButton.place(width=40, height=40, x=190, y=255)

    def cancel(self):
        self.master.image.cv2Image = copy.deepcopy(self.master.image.copy)
        self.master.update_visible_image()
        self.master.image.fill_histogram()
        self.master.update_child_windows()
        self.destroy()