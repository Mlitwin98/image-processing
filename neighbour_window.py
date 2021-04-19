import copy
from tkinter import Label, StringVar, Toplevel
from tkinter.ttk import Button, OptionMenu
from icons_import import saveIcon, closeIcon

class NewNeighbourWindow(Toplevel):
    def __init__(self, master = None, option=None): 
        super().__init__(master = master)   

        self.set_basic(option)
        self.set_operations()
        self.set_widgets()         

        
    def set_basic(self, option):
        self.minsize(400, 400)
        self.maxsize(400, 400)
        self.title("Operacje sąsiedztwa")
        self.option = option

    def set_operations(self):
        operationsSmooth = {
            "Blurr": 2+2,
            "Gaussian Blurr": 2+2,
        }

        operationsEdges = {
            "Sobel": 2+2,
            "Laplacian": 2+2,
            "Canny": 2+2,
        }
        operationsSharpen = {
            "Wyostrzająca 1": 2+2,
            "Wyostrzająca 2": 2+2,
            "Wyostrzająca 3": 2+2,
        }
        operationsEdgesPrewitt = {
            "Prewitt N": 2+2,
            "Prewitt NE": 2+2,
            "Prewitt E": 2+2,
            "Prewitt SE": 2+2,
            "Prewitt S": 2+2,
            "Prewitt SW": 2+2,
            "Prewitt W": 2+2,
            "Prewitt NW": 2+2,
        }
        operationsMedian = {
            "Medianowa 3x3": 2+2,
            "Medianowa 5x5": 2+2,
            "Medianowa 7x7": 2+2,
        }
        operationsCustom = {
            "Własna...": 2+2,
        }

        operationsArray = [operationsSmooth, operationsEdges, operationsSharpen, operationsEdgesPrewitt, operationsMedian, operationsCustom]
        self.operations = operationsArray[self.option]
        self.marginPixelsOptions = {
            "Bez zmian(isolated)": 2+2,
            "Odbicie lustrzane(reflect)": 2+2,
            "Powielenie skrajnych pikseli(replicate)": 2+2,
        }

    def set_widgets(self):
        self.operationChoice = StringVar(self)
        self.pixelChoice = StringVar(self)

        self.operationList = OptionMenu(self, self.operationChoice)
        self.marginPixelList = OptionMenu(self, self.pixelChoice)

        
        self.operationChoice.set(list(self.operations.keys())[0])
        self.marginPixelList.set(list(self.marginPixelsOptions.keys())[0])
        for oper in list(self.operations.keys()):
            self.operationList['menu'].add_command(label=oper, command=lambda v=oper: self.operationChoice.set(v))
        for option in list(self.marginPixelsOptions.keys()):
            self.marginPixelList['menu'].add_command(label=option, command=lambda v=option: self.pixelChoice.set(v))

        self.saveButton = Button(self, image=saveIcon, command=self.update_image)
        self.cancelButton = Button(self, image=closeIcon, command=self.cancel)

        self.place_widgets()

    def update_image(self):
        self.cancel()

    def place_widgets(self):
        Label(self, text="Operacja: ").place(relx=0.05, y=7)

        Label(self, text="Piksele skrajne: ").place(relx=0.05, y=77)

        self.operationList.place(y=5, relx=0.35)
        self.marginPixelList.place(y=40, relx=0.35)


        self.saveButton.place(width=50, height=50, x=0.4, y=340)
        self.cancelButton.place(width=50, height=50, x=0.6, y=340)

    def cancel(self):
        self.master.image.cv2Image = copy.deepcopy(self.master.image.copy)
        self.master.update_visible_image()
        self.master.image.fill_histogram()
        self.master.update_child_windows()
        self.master.thresholdScaleWindow = None
        self.destroy()   
        