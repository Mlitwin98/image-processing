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
        self.geometry('400x100')
        self.minsize(400, 100)
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
        Label(self.write_frame, text='Value: ', borderwidth=2, relief="raised", width=6, height=2).grid(row = 0, column=0)
        Label(self.write_frame, text='Count: ', borderwidth=2, relief="raised", width=6, height=2).grid(row = 1, column=0)
        for value,count in enumerate(image.lut):
            Label(self.write_frame, text=value, borderwidth=2, relief="raised", width=5, height=2).grid(row=0, column=value+1)
            Label(self.write_frame, text=count, borderwidth=2, relief="raised", width=5, height=2).grid(row=1, column=value+1)

        