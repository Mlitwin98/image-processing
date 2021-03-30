from tkinter import Canvas, Frame, Label
from tkinter import Toplevel
from tkinter import ttk
from tkinter.constants import BOTH, BOTTOM, HORIZONTAL, LEFT, X,  NW
from numpy import ndenumerate

class NewLutWindow(Toplevel):
    def __init__(self, name, master = None): 
        super().__init__(master = master)
        self.set_basic(name)
    
        self.display_lut_values()
        self.protocol("WM_DELETE_WINDOW", lambda: self.report_close_to_master())
        

    def set_basic(self, name):
        if self.master.image.isGrayScale:
            self.geometry('500x95')
            self.minsize(500, 95)
        else:
            self.geometry('500x210')
            self.minsize(500, 210)
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
        

    def display_lut_values(self):
        fontsize = 10
        for wg in self.write_frame.winfo_children():
            wg.destroy()
        if self.master.image.isGrayScale:
            Label(self.write_frame, text='Wartość:', font=("Helvetica", fontsize), borderwidth=2, relief="raised", width=8, height=2, bg="gray").grid(row = 0, column=0)
            Label(self.write_frame, text='Zliczenia:', font=("Helvetica", fontsize), borderwidth=2, relief="raised", width=8, height=2).grid(row = 1, column=0)
            for value,count in ndenumerate(self.master.image.lut):
                Label(self.write_frame, text=value[0], font=("Helvetica", fontsize), borderwidth=2, relief="raised", width=5, height=2, bg="gray").grid(row=0, column=value[0]+1)
                Label(self.write_frame, text=count, font=("Helvetica", fontsize), borderwidth=2, relief="raised", width=5, height=2).grid(row=1, column=value[0]+1)
        else:
            Label(self.write_frame, text='Wartość:', font=("Helvetica", fontsize), borderwidth=2, relief="raised", width=9, height=2, bg="gray").grid(row = 0, column=0)
            Label(self.write_frame, text='Red:', font=("Helvetica", fontsize), borderwidth=2, relief="raised", width=9, height=2, bg='red').grid(row = 1, column=0)
            Label(self.write_frame, text='Green:', font=("Helvetica", fontsize), borderwidth=2, relief="raised", width=9, height=2, bg='green').grid(row = 2, column=0)
            Label(self.write_frame, text='Blue:', font=("Helvetica", fontsize), borderwidth=2, relief="raised", width=9, height=2, bg='blue').grid(row = 3, column=0)
            Label(self.write_frame, text='Suma:', font=("Helvetica", fontsize), borderwidth=2, relief="raised", width=9, height=2).grid(row = 4, column=0)
            for value, count in enumerate(self.master.image.lut):
                Label(self.write_frame, text=value, borderwidth=2, font=("Helvetica", fontsize), relief="raised", width=5, height=2, bg="gray").grid(row=0, column=value+1)
                Label(self.write_frame, text=count[0], borderwidth=2, font=("Helvetica", fontsize), relief="raised", width=5, height=2).grid(row=1, column=value+1)
                Label(self.write_frame, text=count[1], borderwidth=2, font=("Helvetica", fontsize), relief="raised", width=5, height=2).grid(row=2, column=value+1)
                Label(self.write_frame, text=count[2], borderwidth=2, font=("Helvetica", fontsize), relief="raised", width=5, height=2).grid(row=3, column=value+1)
                Label(self.write_frame, text=sum(count), borderwidth=2, font=("Helvetica", fontsize), relief="raised", width=5, height=2).grid(row=4, column=value+1)


    def report_close_to_master(self):
        self.master.lutWindow = None
        self.destroy()

        