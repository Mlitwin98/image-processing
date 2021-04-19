import copy
from tkinter import Entry, Label, StringVar, Toplevel
from tkinter.ttk import Button, OptionMenu
from icons_import import saveIcon, closeIcon

class NewNeighbourWindow(Toplevel):
    def __init__(self, master = None, option=None): 
        super().__init__(master = master)   

        self.set_basic(option)
        self.set_operations()
        self.set_widgets()         

        
    def set_basic(self, option):
        self.minsize(400, 500)
        self.maxsize(400, 500)
        self.title("Operacje sąsiedztwa")
        self.option = option

    def set_operations(self):
        operationsSmooth = {
            "Blurr3x3": [[0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,"1/9","1/9","1/9",0,0], [0,0,"1/9","1/9","1/9",0,0], [0,0,"1/9","1/9","1/9",0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0]],
            "Gaussian Blurr": [[0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0]],
        }
        operationsEdges = {
            "Sobel": [[0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0]],
            "Laplacian": [[0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,1,0,0,0], [0,0,1,-4,1,0,0], [0,0,0,1,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0]],
            "Canny": [[0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0]],
            "Prewitt N": [[0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,1,1,1,0,0], [0,0,0,0,0,0,0], [0,0,-1,-1,-1,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0]],
            "Prewitt NE": [[0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,1,1,0,0], [0,0,-1,0,1,0,0], [0,0,-1,-1,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0]],
            "Prewitt E": [[0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,-1,0,1,0,0], [0,0,-1,0,1,0,0], [0,0,-1,0,1,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0]],
            "Prewitt SE": [[0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,-1,-1,0,0,0], [0,0,-1,0,1,0,0], [0,0,0,1,1,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0]],
            "Prewitt S": [[0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,-1,-1,-1,0,0], [0,0,0,0,0,0,0], [0,0,1,1,1,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0]],
            "Prewitt SW": [[0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,-1,-1,0,0], [0,0,1,0,-1,0,0], [0,0,1,1,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0]],
            "Prewitt W": [[0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,1,0,-1,0,0], [0,0,1,0,-1,0,0], [0,0,1,0,-1,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0]],
            "Prewitt NW": [[0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,1,1,0,0,0], [0,0,1,0,-1,0,0], [0,0,0,-1,-1,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0]],
        }
        operationsSharpen = {
            "Wyostrzająca 1": [[0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,-1,0,0,0], [0,0,-1,5,-1,0,0], [0,0,0,-1,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0]],
            "Wyostrzająca 2": [[0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,-1,-1,-1,0,0], [0,0,-1,9,-1,0,0], [0,0,-1,-1,-1,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0]],
            "Wyostrzająca 3": [[0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,1,-2,1,0,0], [0,0,-2,5,-2,0,0], [0,0,1,-2,1,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0]],
        }
        operationsMedian = {
            "Medianowa 3x3": [[0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0]],
            "Medianowa 5x5": [[0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0]],
            "Medianowa 7x7": [[0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0]],
        }
        operationsCustom = {
            "Własna...": [[0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,0,0,0,0]],
        }

        operationsArray = [operationsSmooth, operationsEdges, operationsSharpen, operationsMedian, operationsCustom]
        self.operations = operationsArray[self.option]
        self.marginPixelsOptions = {
            "Bez zmian(isolated)": 0,
            "Odbicie lustrzane(reflect)": 1,
            "Powielenie skrajnych pikseli(replicate)": 2,
        }

    def set_widgets(self):
        self.operationChoice = StringVar(self)
        self.pixelChoice = StringVar(self)
        self.maskVar = [StringVar(self) for _ in range(49)]
        self.maskEntries = [Entry(self, textvariable=self.maskVar[i], justify='center', font=("Helvetica", 15), state='disabled'if self.option != 4 else 'normal') for i in range(49)]

        self.operationList = OptionMenu(self, self.operationChoice)
        self.marginPixelList = OptionMenu(self, self.pixelChoice)

        
        self.operationChoice.set(list(self.operations.keys())[0])
        self.pixelChoice.set(list(self.marginPixelsOptions.keys())[0])
        for oper in list(self.operations.keys()):
            self.operationList['menu'].add_command(label=oper, command=lambda v=oper: self.update_mask(v))
        for option in list(self.marginPixelsOptions.keys()):
            self.marginPixelList['menu'].add_command(label=option, command=lambda v=option: self.pixelChoice.set(v))

        self.saveButton = Button(self, image=saveIcon, command=self.update_image)
        self.cancelButton = Button(self, image=closeIcon, command=self.cancel)

        self.place_widgets()

    def update_image(self):
        self.cancel()

    def update_mask(self, v):
        self.operationChoice.set(v)
        for i in range(7):
            for j in range(7):
                self.maskVar[i*7+j].set(self.operations[self.operationChoice.get()][i][j])

    def place_widgets(self):
        Label(self, text="Operacja: ").place(relx=0.05, y=7)
        Label(self, text="Piksele skrajne: ").place(relx=0.05, y=42)
        self.operationList.place(y=5, relx=0.35)
        self.marginPixelList.place(y=40, relx=0.35)

        for i in range(7):
            for j in range(7):
                self.maskEntries[i*7+j].place(width=50, height=50, x=j*50+25, y=i*50+75)
                self.maskVar[i*7+j].set(self.operations[self.operationChoice.get()][i][j])


        self.saveButton.place(width=50, height=50, x=125, y=440)
        self.cancelButton.place(width=50, height=50, x=225, y=440)

    def cancel(self):
        self.master.image.cv2Image = copy.deepcopy(self.master.image.copy)
        self.master.update_visible_image()
        self.master.image.fill_histogram()
        self.master.update_child_windows()
        self.master.thresholdScaleWindow = None
        self.destroy()   
        