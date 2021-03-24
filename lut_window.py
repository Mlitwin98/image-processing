from tkinter import Canvas, Frame, Label
from tkinter import Toplevel
from tkinter import ttk
from tkinter.constants import BOTH, BOTTOM, HORIZONTAL, LEFT, X,  NW

class NewLutWindow(Toplevel):
    def __init__(self, image, name, master = None): 
        super().__init__(master = master)
        self.set_basic(image, name)
    
        self.display_lut_values(image)
        

    def set_basic(self, image, name):
        self.image = image
        if image.isGrayScale:
            self.geometry('400x100')
            self.minsize(400, 100)
        else:
            self.geometry('400x200')
            self.minsize(400, 200)
        self.maxsize(self.winfo_screenwidth(), 100)
        self.title("LUT {}".format(name))
        self.set_scrollbar()
        
    def set_scrollbar(self):
        mainframe = Frame(self)
        mainframe.pack(fill=BOTH, expand=1, padx=5)
        lutCanvas = Canvas(mainframe)
        lutCanvas.pack(side=LEFT, fill=BOTH, expand = 1)
        scroll = ttk.Scrollbar(lutCanvas, orient=HORIZONTAL, command=lutCanvas.xview)
        scroll.pack(side=BOTTOM, fill=X)

        lutCanvas.configure(xscrollcommand=scroll.set)
        lutCanvas.bind('<Configure>', lambda e: lutCanvas.configure(scrollregion=lutCanvas.bbox('all')))

        def _on_mouse_wheel(event):
            lutCanvas.xview_scroll(-1 * int((event.delta / 120)), "units")

        lutCanvas.bind_all("<MouseWheel>", _on_mouse_wheel)

        self.write_frame = Frame(lutCanvas)
        lutCanvas.create_window((0, 0), window=self.write_frame, anchor=NW)
        

    def display_lut_values(self, image):
        if image.isGrayScale:
            Label(self.write_frame, text='Wartość: ', borderwidth=2, relief="raised", width=6, height=2, bg="gray").grid(row = 0, column=0)
            Label(self.write_frame, text='Zliczenia: ', borderwidth=2, relief="raised", width=6, height=2).grid(row = 1, column=0)
            for value,count in enumerate(image.lut):
                Label(self.write_frame, text=value, borderwidth=2, relief="raised", width=5, height=2, bg="gray").grid(row=0, column=value+1)
                Label(self.write_frame, text=count, borderwidth=2, relief="raised", width=5, height=2).grid(row=1, column=value+1)
        else:
            Label(self.write_frame, text='Wartość: ', borderwidth=2, relief="raised", width=10, height=2, bg="gray").grid(row = 0, column=0)
            Label(self.write_frame, text='Red: ', borderwidth=2, relief="raised", width=10, height=2, bg='red').grid(row = 1, column=0)
            Label(self.write_frame, text='Green: ', borderwidth=2, relief="raised", width=10, height=2, bg='green').grid(row = 2, column=0)
            Label(self.write_frame, text='Blue: ', borderwidth=2, relief="raised", width=10, height=2, bg='blue').grid(row = 3, column=0)
            Label(self.write_frame, text='Suma: ', borderwidth=2, relief="raised", width=10, height=2).grid(row = 4, column=0)
            for value, count in enumerate(image.lut):
                Label(self.write_frame, text=value, borderwidth=2, relief="raised", width=5, height=2, bg="gray").grid(row=0, column=value+1)
                Label(self.write_frame, text=count[0], borderwidth=2, relief="raised", width=5, height=2).grid(row=1, column=value+1)
                Label(self.write_frame, text=count[1], borderwidth=2, relief="raised", width=5, height=2).grid(row=2, column=value+1)
                Label(self.write_frame, text=count[2], borderwidth=2, relief="raised", width=5, height=2).grid(row=3, column=value+1)
                Label(self.write_frame, text=sum(count), borderwidth=2, relief="raised", width=5, height=2).grid(row=4, column=value+1)

        