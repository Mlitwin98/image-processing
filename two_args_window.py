from tkinter import StringVar, Toplevel
from tkinter.ttk import Button, OptionMenu
from icons_import import saveIcon, closeIcon

class NewTwoArgsWindow(Toplevel):
    images = []
    def __init__(self, master = None): 
        super().__init__(master = master)   
        self.set_basic()
        self.set_widgets()         

        
    def set_basic(self):
        self.minsize(200, 200)
        self.maxsize(200, 200)
        self.title("Operacje logiczne")

    def set_widgets(self):
        openFilesNames = [file.name for file in NewTwoArgsWindow.images]
        self.firstChoice = StringVar(self)
        self.firstChoice.set(openFilesNames[0])
        self.secondChoice = StringVar(self)
        self.secondChoice.set(openFilesNames[0])
        self.operationChoice = StringVar(self)
        operations = ["DODAJ", "ODEJMIJ", "ZMIESZAJ", "AND", "OR", "XOR"]
        self.operationChoice.set(operations[0])

        self.firstImageList = OptionMenu(self, self.firstChoice, *openFilesNames)   
        self.secondImageList = OptionMenu(self, self.secondChoice, *openFilesNames)
        self.operationList = OptionMenu(self, self.operationChoice, *operations)

        self.firstImageList.place(y=5, relx=0.25)
        self.operationList.place(y=40, relx=0.25)
        self.secondImageList.place(y=75, relx=0.25)

        self.saveButton = Button(self, image=saveIcon, command=lambda: self.update_image())
        self.cancelButton = Button(self, image=closeIcon, command=lambda: self.cancel())
        self.saveButton.place(width=40, height=40, x=50, y=150)
        self.cancelButton.place(width=40, height=40, x=110, y=150)

    def update_image(self):
        pass

    def cancel(self):
        self.destroy()

    #NIE DODAJE
    def update_list(self):
        openFilesNames = [file.name for file in NewTwoArgsWindow.images]
        self.firstImageList = OptionMenu(self, self.firstChoice, *openFilesNames)   
        self.secondImageList = OptionMenu(self, self.secondChoice, *openFilesNames)
        