from tkinter import filedialog
from classes import NewImageWindow

def import_image(root):
    path = filedialog.askopenfilename()
    if len(path) > 0:
        NewImageWindow(root, path, path)        
    

