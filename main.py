import tkinter as tk
from tkinter import StringVar
from files_options import import_image
from operate import create_hist

FILE_OPTIONS = [
    'Otwórz',
]

FILE_OPTION_TO_FUNC = {
    'Otwórz': lambda:import_image(),
}

root = tk.Tk()
canvas = tk.Canvas(root, height=50, width=600)
canvas.pack()

#Drop down do zrobienia
#variable = StringVar(root)
#variable.set("Plik")
#w = tk.OptionMenu(root, variable, *FILE_OPTIONS, command=get_clicked)
#w.pack()


btnOpen = tk.Button(canvas, text="Otwórz", command= lambda: import_image(root))
btnHist = tk.Button(canvas, text="Histogram", command= lambda: create_hist())


btnOpen.place(width=100, relheight=0.5, x=0, rely=0, anchor=tk.NW)
btnHist.place(width=100, relheight=0.5, x=100, rely=0, anchor=tk.NW)




tk.mainloop()