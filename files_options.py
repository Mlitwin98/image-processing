from tkinter import filedialog
from tkinter import messagebox
import os
from image_window import NewImageWindow
import imghdr

def import_image(root):
    path = filedialog.askopenfilename()
    if len(path) > 0:
        """
        JEŻELI BEDZIE TRZEBA SERIO OTWIERAĆ BMP W TEN SPOSÓB, LINK W ZAKŁADCE
        fil = open(path, 'rb')
        print(fil)
        img = np.fromfile(fil, dtype=np.imag, count=65536)
        print(img.size)
        """
        if imghdr.what(path) is not None:
            NewImageWindow(root, path, os.path.split(path)[1])     
        else:
            messagebox.showerror("Błąd", "Wprowadź poprawny plik")