from tkinter import Canvas, IntVar, Toplevel, Menu, messagebox, filedialog
from tkinter.constants import DISABLED, LEFT, NW, NORMAL
import cv2
import os
from PIL import Image, ImageTk

from state_manager import StateManager
from image_saved import ImageSaved
from histogram_window import NewHistogramWindow
from lut_window import NewLutWindow
from line_profle_window import NewLineProfileWindow
from slider_window import NewSliderWindow, NewAdaptiveSliderWindow
from posterize_window import NewPosterizeWindow
from two_args_window import NewTwoArgsWindow
from custom_mask_window import NewCustomMaskWindow, NewCustomMaskWindowConv
from custom_stretch_window import NewCustomStretchWindow
from morph_window import NewMorphWindow
from morph_line_window import NewMorphLineWindow
from moments_window import NewMomentsWindow

class NewImageWindow(Toplevel):
    def __init__(self, master = None, pathToImage = None, name=None, image=None): 
        super().__init__(master = master)

        if pathToImage is not None and image is None:
            self.pathToImage = pathToImage
            self.image = ImageSaved(pathToImage)
        elif image is not None:
            self.image = image

        self.manager = StateManager(self.image.cv2Image)
        self.set_images()
        self.set_geometry()
        self.set_basic(master, name)
        self.place_menu()
        self.manage_line_profile()
        self.bind_functions()

    # BASICS
    def create_another(self, master, pathToImage, name, image):
        NewImageWindow(master, pathToImage, name, image)

    def set_geometry(self):
        self.minsize(self.imageFromArray.width, self.imageFromArray.height)
        self.geometry('{}x{}'.format(self.imageFromArray.width, self.imageFromArray.height)) 
    
    def set_images(self):        
        self.imageFromArray = Image.fromarray(self.image.cv2Image)
        self.imageCopy = self.imageFromArray.copy()

    def set_basic(self, master, name):
        self.focus_force()
        self.master = master
        self.name = name 
        self.title(name) 
        self.imagePanel = Canvas(self)
        self.imagePanel.place(relwidth=1, relheight = 1, x=0, y=0)

        self.profileWindow = None
        self.histogramWindow = None
        self.lutWindow = None
        self.thresholdScaleWindow = None
        self.posterizeWindow = None
        self.neighborWindow = None
        NewTwoArgsWindow.images[self] = self.name
        for widget in self.master.winfo_children():
            if(type(widget) == NewTwoArgsWindow):
                widget.update_list()
                break

    
    def manage_line_profile(self):
        self.lineCoords = {"x":0,"y":0,"x2":0,"y2":0}
        self.line = None

    def bind_functions(self):
        #Zmieni?? resize'owanie, aktualnie nie pasuje do linii profilu
        self.bind('<Configure>', self.resize_img)
        self.bind('<Control-d>', lambda event: self.duplicate_window())
        self.bind('<Control-z>', lambda event: self.undo())
        self.bind('<Control-y>', lambda event: self.redo())
        self.bind('<Control-s>', lambda event: self.save())
        self.bind("<ButtonPress-3>", self.click)
        self.bind("<B3-Motion>", self.drag)
        self.protocol("WM_DELETE_WINDOW", lambda:self.report_close_to_windows())

    def undo(self):
        self.image.cv2Image = self.manager.undo()
        self.image.copy = self.image.cv2Image
        self.image.fill_histogram()
        self.update_visible_image()
        self.update_child_windows()

    def save(self):
        try:
            cv2.imwrite(self.pathToImage, self.image.cv2Image)
        except AttributeError:
            self.save_as()

    def save_as(self):
        try:
            ext = self.image.file_extension
        except AttributeError:
            ext = '.bmp'
        finally:
            dir = ''
            dir = filedialog.asksaveasfilename(
            initialfile='*'+ext,
            defaultextension=ext, 
            filetypes=[
                ('JPEG', '*.jpg'), 
                ('PNG', '*.png'), 
                ('BMP', '*.bmp'), 
                ('GIF', '*.gif'),
                ]
            )
            if dir != '':
                try:
                    
                    cv2.imwrite(dir, self.image.cv2Image)
                    self.pathToImage = dir
                    self.name = os.path.split(dir)[1]
                    self.title(self.name)
                except cv2.error:
                    messagebox.showerror("B????d", "Nieoczekiwany b????d, sprawd?? czy dobrze wprowadzi??e?? nazw?? pliku")


    def redo(self):
        self.image.cv2Image = self.manager.redo()
        self.image.copy = self.image.cv2Image
        self.image.fill_histogram()
        self.update_visible_image()
        self.update_child_windows()

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
        NewImageWindow(self.master, None, self.name + '(Kopia)', ImageSaved(None,self.image.cv2Image)).focus_set()
    
    def place_menu(self):
        topMenu = Menu(self)
        self.dsc = Menu(topMenu, tearoff=False)
        histMan = Menu(topMenu, tearoff=False)
        
        imageMan = Menu(topMenu, tearoff=False)
        imageAnalize = Menu(topMenu, tearoff=False)
        pointOper = Menu(imageMan, tearoff=False)

        neighborOper = Menu(imageMan, tearoff=False)
        smooth = Menu(neighborOper, tearoff=False)
        detectEdges = Menu(neighborOper, tearoff=False)
        prewitt = Menu(neighborOper, tearoff=False)
        sharpen = Menu(neighborOper, tearoff=False)
        medianM = Menu(neighborOper, tearoff=False)


        imageMan.add_cascade(label="Jednoargumentowe", menu=pointOper)
        imageMan.add_command(label="Dwuargumentowe", compound=LEFT, command=self.create_two_args_window)
        imageMan.add_cascade(label="S??siedztwa", menu=neighborOper)
        imageMan.add_command(label="Morfologiczne", compound=LEFT, command=self.create_morph_window)
        imageMan.add_command(label="Morfologiczna ekstrakcja linii", compound=LEFT, command=self.create_morph_line_window)
        imageMan.add_command(label="Watershed", compound=LEFT, command=self.handle_watershed)
        
        # Opcje OPISU
        self.dsc.add_command(label='Cofnij', compound=LEFT, accelerator='Ctrl+Z', command=self.undo)
        self.dsc.add_command(label='Powt??rz', compound=LEFT, accelerator='Ctrl+Y', command=self.redo)
        self.dsc.add_command(label='Zapisz', accelerator='Ctrl+S', compound=LEFT, command=self.save)
        self.dsc.add_command(label='Zapisz jako...', accelerator='Ctrl+Shift+S', compound=LEFT, command=self.save_as)
        self.dsc.add_command(label='Histogram', compound=LEFT, command=self.create_histogram_window)
        self.dsc.add_command(label='LUT', compound=LEFT, command=self.create_lut_window)        
        self.dsc.add_command(label='Linia profilu', compound=LEFT, state=DISABLED, command=self.create_profile_window)

        # Opcje MANIPULACJI HISTOGRAMEM
        histMan.add_command(label="Rozci??ganie", compound=LEFT, command=self.stretch_image)
        histMan.add_command(label="Rozci??ganie przedzia??ami", compound=LEFT, command=self.create_stretching_window)
        histMan.add_command(label="Wyr??wnanie", compound=LEFT, command=self.equalize_image)

        # Opcje OPERACJI JEDNOARGUMENTOWYCH
        pointOper.add_command(label="Negacja", compound=LEFT, command=self.negate_image)
        pointOper.add_command(label="Progowanie", compound=LEFT, command=lambda:self.threshold_image("BASIC"))
        pointOper.add_command(label="Progowanie adaptacyjne", compound=LEFT, command=lambda:self.threshold_image("ADAPT"))
        pointOper.add_command(label="Progowanie Otsu", compound=LEFT, command=lambda:self.threshold_image("OTSU"))
        pointOper.add_command(label="Posteryzacja", compound=LEFT, command=self.posterize_image)

        # Opcje OPERACJI S??SIEDZTWA
        neighborOper.add_cascade(label="Wyg??adzanie", menu=smooth)
        neighborOper.add_cascade(label="Detekcja kraw??dzi", menu=detectEdges)
        neighborOper.add_cascade(label="Wyostrzanie", menu=sharpen)
        neighborOper.add_cascade(label="Medianowe", menu=medianM)
        neighborOper.add_command(label="W??asne", compound=LEFT, command=lambda:self.create_custom_mask_window(1))
        neighborOper.add_command(label="W??asne splot", compound=LEFT, command=lambda:self.create_custom_mask_window(0))

        neighborOper.add_separator()
        neighborOper.add_command(label="OPCJE SKRAJNYCH PIKSELI", state='disabled', compound=LEFT)
        self.border = IntVar(self)
        self.border.set(2)
        neighborOper.add_radiobutton(label="Bez zmian (isolated)", variable=self.border, value=0)
        neighborOper.add_radiobutton(label="Odbicie lustrzane (reflect)", variable=self.border, value=1)
        neighborOper.add_radiobutton(label="Powielenie skrajnego piksela (replicate)", variable=self.border, value=2)
        
        smooth.add_command(label="Blur", compound=LEFT, command=lambda:self.handle_neighbor_operations("BLUR", self.border.get())) #POZMIENIA?? COMMANDY
        smooth.add_command(label="Gaussian Blur", compound=LEFT, command=lambda:self.handle_neighbor_operations("GAUSSIAN", self.border.get()))

        detectEdges.add_command(label="Sobel", compound=LEFT, command=lambda:self.handle_neighbor_operations("SOBEL", self.border.get()))
        detectEdges.add_command(label="Laplasjan", compound=LEFT, command=lambda:self.handle_neighbor_operations("LAPLASJAN", self.border.get()))
        detectEdges.add_command(label="Canny", compound=LEFT, command=lambda:self.handle_neighbor_operations("CANNY", self.border.get()))
        detectEdges.add_cascade(label="Prewitt", menu=prewitt)
        
        prewitt.add_command(label="Prewitt N", compound=LEFT, command=lambda:self.handle_neighbor_operations("PRW N", self.border.get()))
        prewitt.add_command(label="Prewitt NE", compound=LEFT, command=lambda:self.handle_neighbor_operations("PRW NE", self.border.get()))
        prewitt.add_command(label="Prewitt E", compound=LEFT, command=lambda:self.handle_neighbor_operations("PRW E", self.border.get()))
        prewitt.add_command(label="Prewitt SE", compound=LEFT, command=lambda:self.handle_neighbor_operations("PRW SE", self.border.get()))
        prewitt.add_command(label="Prewitt S", compound=LEFT, command=lambda:self.handle_neighbor_operations("PRW S", self.border.get()))
        prewitt.add_command(label="Prewitt SW", compound=LEFT, command=lambda:self.handle_neighbor_operations("PRW SW", self.border.get()))
        prewitt.add_command(label="Prewitt W", compound=LEFT, command=lambda:self.handle_neighbor_operations("PRW W", self.border.get()))
        prewitt.add_command(label="Prewitt NW", compound=LEFT, command=lambda:self.handle_neighbor_operations("PRW NW", self.border.get()))

        sharpen.add_command(label="Laplasjan 0/-1/5", compound=LEFT, command=lambda:self.handle_neighbor_operations("LAPLASJAN 1", self.border.get()))
        sharpen.add_command(label="Laplasjan -1/-1/9", compound=LEFT, command=lambda:self.handle_neighbor_operations("LAPLASJAN 2", self.border.get()))
        sharpen.add_command(label="Laplasjan 1/-2/5", compound=LEFT, command=lambda:self.handle_neighbor_operations("LAPLASJAN 3", self.border.get()))

        medianM.add_command(label="Maska 3x3", compound=LEFT, command=lambda:self.handle_neighbor_operations("MEDIAN 3", self.border.get()))
        medianM.add_command(label="Maska 5x5", compound=LEFT, command=lambda:self.handle_neighbor_operations("MEDIAN 5", self.border.get()))
        medianM.add_command(label="Maska 7x7", compound=LEFT, command=lambda:self.handle_neighbor_operations("MEDIAN 7", self.border.get()))        

        # OPECJE ANALIZY
        imageAnalize.add_command(label="Wyznaczenie wektora cech obiekt??w", compound=LEFT, command=self.handle_objects_vector)
        imageAnalize.add_command(label="Klasyfikacja obiekt??w fasoli, ry??u i grochu", compound=LEFT, command=self.handle_classify)

        # DODANIE G????WNYCH ZAK??ADEK
        topMenu.add_cascade(label="Obraz", menu=self.dsc)
        topMenu.add_cascade(label="Manipulacja histogramem", menu=histMan)
        topMenu.add_cascade(label="Operacje", menu=imageMan)
        topMenu.add_cascade(label="Analiza", menu=imageAnalize)

        self.config(menu = topMenu)
    
    def update_visible_image(self):
        self.set_images()
        self.photoImage = ImageTk.PhotoImage(self.imageFromArray)
        self.imagePanel.delete("all")
        self.imagePanel.create_image(0, 0, anchor=NW, image=self.photoImage)
    # -------------------

    # SET CHILD WINDOWS
    def create_moments_window(self, colours, moments, areas, lengths, aspectRatios, extents, solidities, equivalentDiameters):
        for widget in self.winfo_children():
            if(type(widget) == NewMomentsWindow):
                widget.lift()
                widget.focus_set()
                return
        wg = NewMomentsWindow(self, colours, moments, areas, lengths, aspectRatios, extents, solidities, equivalentDiameters)
        wg.focus_set()

    def create_morph_window(self):
        if not self.image.check_if_binary():
            messagebox.showerror("B????d", "Obraz musi by?? binarny. Wykonaj posteryzacj?? dla warto??ci 2 i spr??buj ponownie.")
            return
        for widget in self.winfo_children():
            if(type(widget) == NewMorphWindow):
                widget.lift()
                widget.focus_set()
                return
        wg = NewMorphWindow(self)
        wg.focus_set()

    def create_morph_line_window(self):
        for widget in self.winfo_children():
            if(type(widget) == NewMorphLineWindow):
                widget.lift()
                widget.focus_set()
                return
        wg = NewMorphLineWindow(self)
        wg.focus_set()

    def create_custom_mask_window(self, option):
        if option == 1:
            for widget in self.winfo_children():
                if(type(widget) == NewCustomMaskWindow):
                    widget.lift()
                    widget.focus_set()
                    return
            wg = NewCustomMaskWindow(self)
            wg.focus_set()
        elif option == 0:
            for widget in self.winfo_children():
                if(type(widget) == NewCustomMaskWindowConv):
                    widget.lift()
                    widget.focus_set()
                    return
            wg = NewCustomMaskWindowConv(self)
            wg.focus_set()

    def create_two_args_window(self):
        for widget in self.master.winfo_children():
            if(type(widget) == NewTwoArgsWindow):
                widget.lift()
                widget.focus_set()
                return
        wg = NewTwoArgsWindow(self.master)
        wg.focus_set()

    def create_profile_window(self):
        if(self.profileWindow is not None):
            self.profileWindow.lift()
            self.profileWindow.focus_set()
            return
        self.profileWindow = NewLineProfileWindow(self.name, self.lineCoords, self)
        
    def create_histogram_window(self):
        if(self.histogramWindow is not None):
            self.histogramWindow.lift()
            self.histogramWindow.focus_set()
            return
        self.histogramWindow = NewHistogramWindow(self.name, self)

    def create_stretching_window(self):
        for widget in self.winfo_children():
            if(type(widget) == NewCustomStretchWindow):
                widget.lift()
                widget.focus_set()
                return
        wg = NewCustomStretchWindow(self)
        wg.focus_set()

    def create_lut_window(self):
        if(self.lutWindow is not None):
            self.lutWindow.lift()
            self.lutWindow.focus_set()
            return
        self.lutWindow = NewLutWindow(self.name, self)

    def update_child_windows(self):
        if self.histogramWindow is not None:
            self.histogramWindow.update_histogram()

        if self.lutWindow is not None:
            self.lutWindow.display_lut_values()

        if self.profileWindow is not None:
            self.profileWindow.update_line(self.lineCoords)

    def resize_child_windows(self):
        offsetX = self.winfo_rootx()-self.winfo_x()
        offsetY = self.winfo_rooty()-self.winfo_y()
        if self.posterizeWindow is not None:
            self.posterizeWindow.geometry('%dx%d+%d+%d' % (self.winfo_width(), self.posterizeWindow.height, self.winfo_x()+offsetX, self.winfo_y()+self.winfo_height()+offsetY+2))
        if self.thresholdScaleWindow is not None:
            self.thresholdScaleWindow.geometry('%dx%d+%d+%d' % (self.thresholdScaleWindow.width, self.winfo_height(),self.winfo_x()+self.winfo_width()+offsetX+2, self.winfo_y()+offsetY))
    # -------------------

    # ONE CLICK OPERATIONS
    def handle_classify(self):
        self.image.classify()
        self.manager.new_state(self.image.cv2Image)
        self.update_visible_image()
        self.update_child_windows()
        messagebox.showinfo("LEGENDA", "Zielony = ryz \n Niebieski = soczewica \n Czerwony = fasola")

    def handle_objects_vector(self):
        colours, moments, areas, lengths, aspectRatios, extents, solidities, equivalentDiameters = self.image.get_objects_vector()
        self.manager.new_state(self.image.cv2Image)
        self.update_visible_image()
        self.update_child_windows()
        self.create_moments_window(colours, moments, areas, lengths, aspectRatios, extents, solidities, equivalentDiameters)

    def handle_watershed(self):
        self.image.my_watershed()
        self.image.copy = self.image.cv2Image
        self.manager.new_state(self.image.cv2Image)
        self.update_visible_image()
        self.update_child_windows()

    def equalize_image(self):
        self.image.equalize()
        self.manager.new_state(self.image.cv2Image)
        self.update_visible_image()
        self.update_child_windows()

    def stretch_image(self, oldMin=None, oldMax=None, newMini=None, newMaxi=None):
        self.image.stretch(oldMin, oldMax, newMini, newMaxi)
        self.manager.new_state(self.image.cv2Image)
        self.update_visible_image()
        self.update_child_windows()

    def negate_image(self):
        self.image.negate()
        self.manager.new_state(self.image.cv2Image)
        self.update_visible_image()
        self.update_child_windows()

    def threshold_image(self, method):
        if method == "BASIC":
            if self.thresholdScaleWindow is None:
                self.thresholdScaleWindow = NewSliderWindow(self)
            else:
                self.thresholdScaleWindow.cancel()
                self.thresholdScaleWindow = NewSliderWindow(self)
        elif method == "ADAPT":
            if self.thresholdScaleWindow is None:
                self.thresholdScaleWindow = NewAdaptiveSliderWindow(self)
            else:
                self.thresholdScaleWindow.cancel()
                self.thresholdScaleWindow = NewAdaptiveSliderWindow(self)
        elif method == "OTSU":
            self.image.threshold_otsu()
            self.manager.new_state(self.image.cv2Image)
            self.update_visible_image()
            self.update_child_windows()

    def posterize_image(self):
        if self.posterizeWindow is None:
            self.posterizeWindow = NewPosterizeWindow(self.name, self)
            self.manager.new_state(self.image.cv2Image)
            self.update_visible_image()
            self.update_child_windows()

    def handle_neighbor_operations(self, operation, borderOption):
        self.image.neighbor_operations(operation, borderOption)
        self.manager.new_state(self.image.cv2Image)
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