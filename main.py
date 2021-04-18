from tkinter import Tk, Canvas, Menu, mainloop, ttk
root = Tk()
from tkinter.constants import LEFT
from files_options import import_image


root.title("APO")
style = ttk.Style(root)
style.theme_use('alt')
canvas = Canvas(root, height=0, width=200)
canvas.pack()

top_menu = Menu()

# PLIK (otwórz, zapisz, etc.)
file = Menu(top_menu, tearoff=False)
file.add_command(label='Nowy', compound=LEFT, accelerator='Ctrl+N')
file.add_command(label='Otwórz z...', compound=LEFT, accelerator='Ctrl+O', command= lambda: import_image(root))
file.add_command(label='Zapisz', compound=LEFT, accelerator='Ctrl+S')
file.add_command(label='Zapisz jako...', compound=LEFT, accelerator='Ctrl+Alt+S')

next = Menu(top_menu, tearoff=False)

top_menu.add_cascade(label='Plik', menu=file)


root.bind_all("<Control-o>", func= lambda x:import_image(root))
root.config(menu=top_menu)
mainloop()