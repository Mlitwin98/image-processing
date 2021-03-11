import tkinter as tk
from files_options import import_image

root = tk.Tk()
root.title("IPLM")
canvas = tk.Canvas(root, height=0, width=200)
canvas.pack()

top_menu = tk.Menu()

# PLIK (otwórz, zapisz, etc.)
file = tk.Menu(top_menu, tearoff=False)
file.add_command(label='Nowy', compound=tk.LEFT, accelerator='Ctrl+N')
file.add_command(label='Otwórz z...', compound=tk.LEFT, accelerator='Ctrl+O', command= lambda: import_image(root))
file.add_command(label='Zapisz', compound=tk.LEFT, accelerator='Ctrl+S')
file.add_command(label='Zapisz jako...', compound=tk.LEFT, accelerator='Ctrl+Alt+S')

next = tk.Menu(top_menu, tearoff=False)

top_menu.add_cascade(label='Plik', menu=file)
top_menu.add_cascade(label='Kolejne okienka', menu=next)


root.bind_all("<Control-o>", func= lambda x:import_image(root))
root.config(menu=top_menu)
tk.mainloop()