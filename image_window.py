from tkinter import Canvas, Toplevel, Menu, IntVar
from tkinter.constants import DISABLED, LEFT, NW, NORMAL
from PIL import Image, ImageTk
from image_saved import ImageSaved
from histogram_window import NewHistogramWindow
from lut_window import NewLutWindow
from line_profle_window import NewLineProfileWindow
from slider_window import NewSliderWindow
from posterize_window import NewPosterizeWindow
from two_args_window import NewTwoArgsWindow

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
        NewTwoArgsWindow.images[self] = self.name
        for widget in self.master.winfo_children():
            if(type(widget) == NewTwoArgsWindow):
                widget.update_list()
                break

    
    def manage_line_profile(self):
        self.lineCoords = {"x":0,"y":0,"x2":0,"y2":0}
        self.line = None

    def bind_functions(self):
        #Zmienić resize'owanie, aktualnie nie pasuje do linii profilu
        self.bind('<Configure>', self.resize_img)
        self.bind('<Control-d>', lambda event: self.duplicate_window())
        self.bind("<ButtonPress-3>", self.click)
        self.bind("<B3-Motion>", self.drag)
        self.protocol("WM_DELETE_WINDOW", lambda: self.report_close_to_windows())

    def report_close_to_windows(self):
        NewTwoArgsWindow.images.pop(self)
        for widget in self.master.winfo_children():
            if(type(widget) == NewTwoArgsWindow):
                widget.update_list()
                break
        self.destroy()
    # -------------------

    # WINDOW
    def duplicate_window(self):
        NewImageWindow(self.master, self.pathToImage, self.name + '(Kopia)')
    
    def place_menu(self):
        topMenu = Menu(self)
        self.dsc = Menu(topMenu, tearoff=False)
        histMan = Menu(topMenu, tearoff=False)
        imageMan = Menu(topMenu, tearoff=False)
        pointOper = Menu(imageMan, tearoff=False)
        neighbOper = Menu(imageMan, tearoff=False)
        imageMan.add_cascade(label="Jednoargumentowe", menu=pointOper)
        imageMan.add_command(label="Dwuargumentowe", compound=LEFT, command=lambda:self.create_two_args_window())
        imageMan.add_cascade(label="Sąsiedztwa", menu=neighbOper)
        
        # Opcje OPISU
        self.dsc.add_command(label='Histogram', compound=LEFT, command= lambda: self.create_histogram_window())
        self.dsc.add_command(label='LUT', compound=LEFT, command= lambda: self.create_lut_window())        
        self.dsc.add_command(label='Linia profilu', compound=LEFT, state=DISABLED, command= lambda: self.create_profile_window())

        # Opcje MANIPULACJI HISTOGRAMEM
        histMan.add_command(label="Rozciąganie", compound=LEFT, command= lambda: self.stretch_image())
        histMan.add_command(label="Wyrównanie", compound=LEFT, command= lambda: self.equalize_image())

        # Opcje OPERACJI JEDNOARGUMENTOWYCH
        pointOper.add_command(label="Negacja", compound=LEFT, command= lambda: self.negate_image())
        pointOper.add_command(label="Progowanie", compound=LEFT, command= lambda: self.threshold_image())
        pointOper.add_command(label="Posteryzacja", compound=LEFT, command= lambda: self.posterize_image())

        # Ustawianie co robić z brzegowymi pikselami (nie wiem czy to dobre wyjście pod względem interfejsu)
        self.radioVar = IntVar()
        self.radioVar.set(0)
        neighbOper.add_radiobutton(label="Wartości brzegowe bez zmian", compound=LEFT, value=0, var=self.radioVar)
        neighbOper.add_radiobutton(label="Padding lustrzany", compound=LEFT, value=1, var=self.radioVar)
        neighbOper.add_radiobutton(label="Padding powielenia", compound=LEFT, value=2, var=self.radioVar)

        # DODANIE GŁÓWNYCH ZAKŁADEK
        topMenu.add_cascade(label="Opis", menu=self.dsc)
        topMenu.add_cascade(label="Manipulacja histogramem", menu=histMan)
        topMenu.add_cascade(label="Operacje", menu=imageMan)

        self.config(menu = topMenu)
    
    def update_visible_image(self):
        self.set_images()
        self.photoImage = ImageTk.PhotoImage(self.imageFromArray)
        self.imagePanel.delete("all")
        self.imagePanel.create_image(0, 0, anchor=NW, image=self.photoImage)
    # -------------------

    # SET CHILD WINDOWS
    def create_two_args_window(self):
        for widget in self.master.winfo_children():
            if(type(widget) == NewTwoArgsWindow):
                widget.lift()
                widget.focus_set()
                return
        wg = NewTwoArgsWindow(self.master)
        wg.focus_set()

    def create_profile_window(self):
        for widget in self.winfo_children():
            if(type(widget) == NewLineProfileWindow):
                widget.lift()
                widget.focus_set()
                return
        self.profileWindow = NewLineProfileWindow(self.name, self.lineCoords, self)
        
    def create_histogram_window(self):
        for widget in self.winfo_children():
            if(type(widget) == NewHistogramWindow):
                widget.lift()
                widget.focus_set()
                return
        self.histogramWindow = NewHistogramWindow(self.name, self)

    def create_lut_window(self):
        for widget in self.winfo_children():
            if(type(widget) == NewLutWindow):
                widget.lift()
                widget.focus_set()
                return
        self.lutWindow = NewLutWindow(self.name, self)

    def update_child_windows(self):
        if self.histogramWindow is not None:
            self.histogramWindow.update_histogram()

        if self.lutWindow is not None:
            self.lutWindow.display_lut_values()

    def resize_child_windows(self):
        offsetX = self.winfo_rootx()-self.winfo_x()
        offsetY = self.winfo_rooty()-self.winfo_y()
        if self.posterizeWindow is not None:
            self.posterizeWindow.geometry('%dx%d+%d+%d' % (self.winfo_width(), self.posterizeWindow.height, self.winfo_x()+offsetX, self.winfo_y()+self.winfo_height()+offsetY+2))
        if self.thresholdScaleWindow is not None:
            self.thresholdScaleWindow.geometry('%dx%d+%d+%d' % (self.thresholdScaleWindow.width, self.winfo_height(),self.winfo_x()+self.winfo_width()+offsetX+2, self.winfo_y()+offsetY))
    # -------------------

    # OPERATIONS
    def equalize_image(self):
        self.image.equalize()
        self.update_visible_image()
        self.update_child_windows()

    def stretch_image(self):
        self.image.stretch()
        self.update_visible_image()
        self.update_child_windows()

    def negate_image(self):
        self.image.negate()
        self.update_visible_image()
        self.update_child_windows()

    def threshold_image(self):
        if self.thresholdScaleWindow is None:
            self.thresholdScaleWindow = NewSliderWindow(self.name, self)

    def posterize_image(self):
        if self.posterizeWindow is None:
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
        self.resize_child_windows()
        #self.newWidth = event.width
        #self.newHeight = event.height
        #self.imageFromArray = self.imageCopy.resize((self.newWidth, self.newHeight))
        self.photoImage = ImageTk.PhotoImage(self.imageFromArray)
        self.imagePanel.create_image(0, 0, anchor=NW, image=self.photoImage)
    # -------------------