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
canvas = Canvas(root, height=0, width=250)
canvas.pack()

top_menu = Menu()

top_menu.add_command(label='Otwórz z...', compound=LEFT, accelerator='Ctrl+O', command= lambda: import_image(root))
top_menu.add_command(label="Informacja o programie", command= lambda: messagebox.showinfo("Informacje", info))

root.bind_all("<Control-o>", func= lambda x:import_image(root))
root.config(menu=top_menu)
mainloop()