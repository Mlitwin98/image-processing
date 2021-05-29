from tkinter import Canvas, Frame, Label, Toplevel, messagebox
from tkinter import ttk
from tkinter.constants import BOTH, LEFT, NW, RIGHT, VERTICAL, Y
from tkinter.ttk import Button

class NewMomentsWindow(Toplevel):
    def __init__(self, master, colours, moments, areas, lengths, aspectRatios, extents, solidities, equivalentDiameters): 
        super().__init__(master = master)   
        self.colours = colours
        self.moments = moments
        self.areas = areas
        self.lengths = lengths
        self.aspectRatios = aspectRatios
        self.extents = extents
        self.solidities = solidities
        self.equivalentDiameters = equivalentDiameters
        self.set_basic()
        self.set_widgets()         

    def set_basic(self):
        self.minsize(870, 400)
        self.maxsize(870, 400)
        self.title("Opis obiektów")    
        self.set_scrollbar()

    def set_scrollbar(self):
        mainframe = Frame(self)
        mainframe.pack(fill=BOTH, expand=1, padx=5)
        self.momentsCanvas = Canvas(mainframe)
        self.momentsCanvas.pack(side=LEFT, fill=BOTH, expand = 1)
        scroll = ttk.Scrollbar(self.momentsCanvas, orient=VERTICAL, command=self.momentsCanvas.yview)
        scroll.pack(side=RIGHT, fill=Y)

        self.momentsCanvas.configure(yscrollcommand=scroll.set)
        self.momentsCanvas.bind('<Configure>', lambda e: self.momentsCanvas.configure(scrollregion=self.momentsCanvas.bbox('all')))

        def _on_mouse_wheel(event):
            self.momentsCanvas.yview_scroll(-1 * int((event.delta / 120)), "units")

        self.momentsCanvas.bind_all("<MouseWheel>", _on_mouse_wheel)

        self.write_frame = Canvas(self.momentsCanvas)
        self.momentsCanvas.create_window((0, 0), window=self.write_frame, anchor=NW)

    def set_widgets(self):
        Label(self.write_frame, text="Obiekt", font=("Helvetica", 15), width=7).grid(row = 0, column=0)
        Label(self.write_frame, text="Momenty", font=("Helvetica", 15), width=7).grid(row = 0, column=1)
        Label(self.write_frame, text="Pole", font=("Helvetica", 15), width=7).grid(row = 0, column=2)
        Label(self.write_frame, text="Obwód", font=("Helvetica", 15), width=7).grid(row = 0, column=3)
        Label(self.write_frame, text="Aspect ratio", font=("Helvetica", 15), width=9).grid(row = 0, column=4)
        Label(self.write_frame, text="Extent", font=("Helvetica", 15), width=7).grid(row = 0, column=5)
        Label(self.write_frame, text="Solidity", font=("Helvetica", 15), width=7).grid(row = 0, column=6)
        Label(self.write_frame, text="Equivalent diameter", font=("Helvetica", 15), width=15).grid(row = 0, column=7)
        for i in range(len(self.colours)):
            Button(self.write_frame, text='M', width=7, command=lambda i=i: messagebox.showinfo(f"Momenty obiektu {i+1}", self.get_moments_formatted(self.moments[i]))).grid(row = i*2+1, rowspan=2, column=1)
            Label(self.write_frame, text=("%.2f"%self.areas[i]), width=10, height=5, font=("Helvetica", 11)).grid(row = i*2+1, rowspan=2, column=2)
            Label(self.write_frame, text=("%.2f"%self.lengths[i]), width=10, height=5, font=("Helvetica", 11)).grid(row = i*2+1, rowspan=2, column=3)
            Label(self.write_frame, text=("%.4f"%self.aspectRatios[i]), width=10, height=5, font=("Helvetica", 11)).grid(row = i*2+1, rowspan=2, column=4)
            Label(self.write_frame, text=("%.4f"%self.extents[i]), width=10, height=5, font=("Helvetica", 11)).grid(row = i*2+1, rowspan=2, column=5)
            Label(self.write_frame, text=("%.4f"%self.solidities[i]), width=10, height=5, font=("Helvetica", 11)).grid(row = i*2+1, rowspan=2, column=6)
            Label(self.write_frame, text=("%.4f"%self.equivalentDiameters[i]), width=10, height=5, font=("Helvetica", 11)).grid(row = i*2+1, rowspan=2, column=7)
            self.write_frame.create_rectangle(20, 50+51*i+40*i, 60, 90+51*i+40*i, fill=self._from_rgb(self.colours[i]))

    def _from_rgb(self, rgb):
        return "#%02x%02x%02x" % rgb 

    def get_moments_formatted(self, moments):
        out = ''
        for moment in moments:
            out += f'{moment}: {moments[moment]} \n'
        return out
 