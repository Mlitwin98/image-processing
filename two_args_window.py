from tkinter import Label, StringVar, Toplevel
from tkinter.ttk import Button, OptionMenu

import numpy as np
from icons_import import saveIcon, closeIcon

class NewTwoArgsWindow(Toplevel):
    images = {}
    def __init__(self, master = None): 
        super().__init__(master = master)   

        self.set_basic()
        self.set_widgets()         

        
    def set_basic(self):
        self.minsize(200, 200)
        self.maxsize(200, 200)
        self.title("Operacje logiczne")

    def set_widgets(self):
        operations = ["DODAJ", "ODEJMIJ", "ZMIESZAJ", "AND", "OR", "XOR"]
        self.firstChoice = StringVar(self)
        self.secondChoice = StringVar(self)
        self.operationChoice = StringVar(self)

        self.firstImageList = OptionMenu(self, self.firstChoice)
        self.secondImageList = OptionMenu(self, self.secondChoice)
        self.operationList = OptionMenu(self, self.operationChoice)

        
        self.update_list()

        self.operationChoice.set(operations[0])
        for oper in operations:
            self.operationList['menu'].add_command(label=oper, command=lambda v=oper: self.operationChoice.set(v))

        self.saveButton = Button(self, image=saveIcon, command=lambda: self.update_image())
        self.cancelButton = Button(self, image=closeIcon, command=lambda: self.cancel())

        self.place_widgets()

    def update_image(self):
        imageWindow1, imageWindow2 = None, None
        for obj, name in NewTwoArgsWindow.images.items():
            if name == self.firstChoice.get():
                imageWindow1 = obj
                if self.firstChoice.get() != self.secondChoice.get():
                    NewTwoArgsWindow.images.pop(obj)
                break

        for obj, name in NewTwoArgsWindow.images.items():
            if name == self.secondChoice.get():
                imageWindow2 = obj

        self.operations = {
            "DODAJ": imageWindow1.image.add,
            "ODEJMIJ": imageWindow1.image.sub,
            "ZMIESZAJ": imageWindow1.image.blend,
            "AND": imageWindow1.image.bit_and,
            "OR": imageWindow1.image.bit_or,
            "XOR": imageWindow1.image.bit_xor,
        }
        self.operations[self.operationChoice.get()](imageWindow2.image)

        #JEŻELI NOWIE OKIENKO TO RÓB NOWE OKIENKO
        imageWindow1.update_visible_image()
        imageWindow1.update_child_windows()
        self.cancel()

    def cancel(self):
        self.destroy()

    def update_list(self):
        if len(NewTwoArgsWindow.images) <= 0:
            self.cancel()
            return
        openFilesNames = list(NewTwoArgsWindow.images.values())
        self.firstChoice.set(openFilesNames[0])
        self.secondChoice.set(openFilesNames[0])            

        self.firstImageList['menu'].delete(0, 'end')
        self.secondImageList['menu'].delete(0, 'end')

        for file in openFilesNames:
            self.firstImageList['menu'].add_command(label=file, command=lambda v=file: self.firstChoice.set(v))
            self.secondImageList['menu'].add_command(label=file, command=lambda v=file: self.secondChoice.set(v))

    def place_widgets(self):
        Label(self, text="Obraz1: ").place(relx=0.05, y=7)
        Label(self, text="Operacja: ").place(relx=0.05, y=42)
        Label(self, text="Obraz2: ").place(relx=0.05, y=77)
        self.firstImageList.place(y=5, relx=0.35)
        self.operationList.place(y=40, relx=0.35)
        self.secondImageList.place(y=75, relx=0.35)

        self.saveButton.place(width=40, height=40, x=50, y=150)
        self.cancelButton.place(width=40, height=40, x=110, y=150)
        