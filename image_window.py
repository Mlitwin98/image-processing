from tkinter import Canvas, Toplevel, Menu
from tkinter.constants import DISABLED, LEFT, NW, NORMAL
from PIL import Image, ImageTk
from image_saved import ImageSaved
from histogram_window import NewHistogramWindow
from lut_window import NewLutWindow
from line_profle_window import NewLineProfileWindow
from slider_window import NewSliderWindow
from posterize_window import NewPosterizeWindow

class NewImageWindow(Toplevel):
    def __init__(self, master = None, pathToImage = None, name=None): 
        super().__init__(master = master)

        self.pathToImage = pathToImage
        self.image = ImageSaved(pathToImage)
        self.set_images()
        self.set_geometry()
        self.set_basic(master, pathToImage, name)
        self.place_menu()
        self.manage_line_profile()
        self.bind_functions()

    # BASICS
    def set_geometry(self):
        self.geometry('{}x{}'.format(self.imageFromArray.width, self.imageFromArray.height))
        self.minsize(200, 200)
    
    def set_images(self):        
        self.imageFromArray = Image.fromarray(self.image.cv2Image)
        self.imageCopy = self.imageFromArray.copy()

    def set_basic(self, master, pathToImage, name):
        self.focus_force()
        self.master = master
        self.path = pathToImage
        self.name = name 
        self.title(name) 
        self.imagePanel = Canvas(self)
        self.imagePanel.place(relwidth=1, relheight = 1, x=0, y=0)

        self.profileWindow = None
        self.histogramWindow = None
        self.lutWindow = None
        self.thresholdScaleWindow = None
        self.posterizeWindow = None

    
    def manage_line_profile(self):
        self.lineCoords = {"x":0,"y":0,"x2":0,"y2":0}
        self.line = None

    def bind_functions(self):
        #Zmienić resize'owanie, aktualnie nie pasuje do linii profilu
        self.bind('<Configure>', self.resize_img)
        self.bind('<Control-d>', lambda event: self.duplicate_window())
        self.bind("<ButtonPress-3>", self.click)
        self.bind("<B3-Motion>", self.drag)
    # -------------------

    # WINDOW
    def duplicate_window(self):
        NewImageWindow(self.master, self.pathToImage, self.name + '(Kopia)')
    
    def place_menu(self):
        topMenu = Menu()

        self.dsc = Menu(topMenu, tearoff=False)
        self.dsc.add_command(label='Histogram', compound=LEFT, command= lambda: self.create_histogram_window())
        self.dsc.add_command(label='LUT', compound=LEFT, command= lambda: self.create_lut_window())        
        self.dsc.add_command(label='Linia profilu', compound=LEFT, state=DISABLED, command= lambda: self.create_profile_window())

        histMan = Menu(topMenu, tearoff=False)
        histMan.add_command(label="Rozciąganie", compound=LEFT, command= lambda: 2+2)
        histMan.add_command(label="Wyrównanie", compound=LEFT, command= lambda: 2+2)

        pointOper = Menu(topMenu, tearoff=False)
        pointOper.add_command(label="Negacja", compound=LEFT, command= lambda: self.negate_image())
        pointOper.add_command(label="Progowanie", compound=LEFT, command= lambda: self.threshold_image())
        pointOper.add_command(label="Posteryzacja", compound=LEFT, command= lambda: self.posterize_image())

        topMenu.add_cascade(label="Opis", menu=self.dsc)
        topMenu.add_cascade(label="Manipulacja histogramem", menu=histMan)
        topMenu.add_cascade(label="Operacje jednopunktowe", menu=pointOper)

        self.config(menu = topMenu)
    
    def update_visible_image(self):
        self.set_images()
        self.photoImage = ImageTk.PhotoImage(self.imageFromArray)
        self.imagePanel.delete("all")
        self.imagePanel.create_image(0, 0, anchor=NW, image=self.photoImage)
    # -------------------

    # SET CHILD WINDOWS
    def create_profile_window(self):
        self.profileWindow = NewLineProfileWindow(self.name, self.lineCoords, [self.newWidth, self.newHeight], self)

    def create_histogram_window(self):
        self.histogramWindow = NewHistogramWindow(self.name, self)

    def create_lut_window(self):
        self.lutWindow = NewLutWindow(self.name, self)

    def update_child_windows(self):
        if self.histogramWindow is not None:
            self.histogramWindow.update_histogram()

        if self.lutWindow is not None:
            self.lutWindow.display_lut_values()
    # -------------------

    # OPERATIONS
    def negate_image(self):
        self.image.negate()
        self.update_visible_image()
        self.update_child_windows()

    def threshold_image(self):
        self.thresholdScaleWindow = NewSliderWindow(self.name, self)
        self.update_visible_image()
        self.update_child_windows()

    def posterize_image(self):
        self.posterizeWindow = NewPosterizeWindow(self.name, self)
        self.update_visible_image()
        self.update_child_windows()
    # -------------------


    # ON EVENT
    def click(self, e):
        self.lineCoords["x"] = e.x
        self.lineCoords["y"] = e.y
        self.dsc.entryconfigure('Linia profilu', state=NORMAL)

    def drag(self, e):
        self.lineCoords["x2"] = e.x
        self.lineCoords["y2"] = e.y
        if self.line is not None:
            self.imagePanel.delete(self.line) 
        self.line = self.imagePanel.create_line(self.lineCoords["x"], self.lineCoords["y"], self.lineCoords['x2'], self.lineCoords['y2'], fill='red', dash=(2, 2))
        
        if self.profileWindow is not None:
            self.profileWindow.update_line(self.lineCoords)

    def resize_img(self, event):
        #self.newWidth = event.width
        #self.newHeight = event.height
        #self.imageFromArray = self.imageCopy.resize((self.newWidth, self.newHeight))
        self.photoImage = ImageTk.PhotoImage(self.imageFromArray)
        self.imagePanel.create_image(0, 0, anchor=NW, image=self.photoImage)
    # -------------------