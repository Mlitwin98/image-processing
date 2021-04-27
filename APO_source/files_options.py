from tkinter import filedialog
from tkinter import messagebox
import os
from image_window import NewImageWindow
import imghdr

def import_image(root):
    path = filedialog.askopenfilename()
    if len(path) > 0:
        if imghdr.what(path) is not None:
            NewImageWindow(root, path, os.path.split(path)[1])     
        else:
            messagebox.showerror("Błąd", "Wprowadź poprawny plik")