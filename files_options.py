from tkinter import filedialog
import os
from image_window import NewImageWindow

def import_image(root):
    path = filedialog.askopenfilename()
    if len(path) > 0:
        NewImageWindow(root, path, os.path.split(path)[1])        
    

