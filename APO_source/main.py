from tkinter import Tk, Canvas, Menu, mainloop, messagebox, ttk
root = Tk()
from tkinter.constants import LEFT
from files_options import import_image

info = """
Aplikacja zbiorcza z ćwiczeń laboratoryjnych i projektu

Tytuł projektu: Udoskonalenie oprogramowania przygotowanego na zajęciach przez wykonanie narzędzia do ekstrakcja linii pionowych i poziomych za pomocą operacji morfologicznych 

Autor: Mateusz Litwin

Prowadzący: mgr inż. Łukasz Roszkowiak

Algorytmy Przetwarzania Obrazów 2021

WIT grupa ID: ID06IO1
"""

root.title("APO")
style = ttk.Style(root)
style.theme_use('alt')
canvas = Canvas(root, height=0, width=200)
canvas.pack()

top_menu = Menu()

file = Menu(top_menu, tearoff=False)
file.add_command(label='Nowy', compound=LEFT, accelerator='Ctrl+N')
file.add_command(label='Otwórz z...', compound=LEFT, accelerator='Ctrl+O', command= lambda: import_image(root))

next = Menu(top_menu, tearoff=False)

top_menu.add_cascade(label='Plik', menu=file)
top_menu.add_command(label="Informacja o programie", command= lambda: messagebox.showinfo("Informacje", info))


root.bind_all("<Control-o>", func= lambda x:import_image(root))
root.config(menu=top_menu)
mainloop()