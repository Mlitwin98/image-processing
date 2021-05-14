import copy
from tkinter import IntVar, Label, StringVar, Toplevel
from tkinter.ttk import Button, Checkbutton, OptionMenu
from image_saved import ImageSaved
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
        self.imageWindow1, self.imageWindow2 = None, None
        self.operations = ["DODAJ","ODEJMIJ","ZMIESZAJ","AND","OR","XOR"]        

    def set_widgets(self):
        self.firstChoice = StringVar(self)
        self.secondChoice = StringVar(self)
        self.operationChoice = StringVar(self)

        self.firstImageList = OptionMenu(self, self.firstChoice)
        self.secondImageList = OptionMenu(self, self.secondChoice)
        self.operationList = OptionMenu(self, self.operationChoice)

        
        self.update_list()
        self.operationChoice.set(self.operations[0])
        for oper in self.operations:
            self.operationList['menu'].add_command(label=oper, command=lambda v=oper: self.operationChoice.set(v))

        self.cbVal = IntVar()
        self.cb = Checkbutton(self, width=0, variable=self.cbVal)

        self.saveButton = Button(self, image=saveIcon, command=self.update_image)
        self.cancelButton = Button(self, image=closeIcon, command=self.cancel)

        self.place_widgets()

    def update_image(self):
        for obj, name in NewTwoArgsWindow.images.items():
            if name == self.firstChoice.get():
                self.imageWindow1 = obj
                break
        for obj, name in NewTwoArgsWindow.images.items():
            if name == self.secondChoice.get():
                self.imageWindow2 = obj
                break

        outputImage = self.imageWindow1.image.two_args_operations(self.operationChoice.get(), self.imageWindow2.image)

        if self.cbVal: 
            windowName = self.imageWindow1.name + " " + self.operationChoice.get() + " " + self.imageWindow2.name
            self.imageWindow1.create_another(self.master, None, windowName, ImageSaved(None,outputImage))
        else:
            self.imageWindow1.image.cv2Image = outputImage
            self.master.image.copy = copy.deepcopy(self.master.image.cv2Image)
            self.imageWindow1.image.fill_histogram()
            self.imageWindow1.manager.new_state(self.imageWindow1.image.cv2Image)
            self.imageWindow1.update_visible_image()
            self.imageWindow1.update_child_windows()
        self.cancel()

    def cancel(self):
        self.destroy()

    def update_list(self):
        if len(NewTwoArgsWindow.images) <= 0:
            self.cancel()
            return
        openFilesNames = list(NewTwoArgsWindow.images.values())
        self.firstChoice.set(openFilesNames[0])
        self.secondChoice.set(openFilesNames[0]) if len(NewTwoArgsWindow.images) == 1 else self.secondChoice.set(openFilesNames[1]) 
             

        self.firstImageList['menu'].delete(0, 'end')
        self.secondImageList['menu'].delete(0, 'end')

        for file in openFilesNames:
            self.firstImageList['menu'].add_command(label=file, command=lambda v=file: self.firstChoice.set(v))
            self.secondImageList['menu'].add_command(label=file, command=lambda v=file: self.secondChoice.set(v))

    def place_widgets(self):
        Label(self, text="Obraz1: ").place(relx=0.05, y=7)
        Label(self, text="Operacja: ").place(relx=0.05, y=42)
        Label(self, text="Obraz2: ").place(relx=0.05, y=77)
        Label(self, text="Obraz wynikowy").place(relx=0.05, y=102)
        Label(self, text="w nowym okienku?").place(relx=0.05, y=120)
        self.firstImageList.place(y=5, relx=0.35)
        self.operationList.place(y=40, relx=0.35)
        self.secondImageList.place(y=75, relx=0.35)

        self.cb.place(y=110, relx=0.7)
        self.cb.invoke()

        self.saveButton.place(width=40, height=40, x=50, y=150)
        self.cancelButton.place(width=40, height=40, x=110, y=150)
        