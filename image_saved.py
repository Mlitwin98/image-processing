import cv2
import numpy as np

class ImageSaved():
    def __init__(self, path):
        self.cv2Image = cv2.imread(path, 1)
        self.isGrayScale = self.check_if_is_gray()
        if self.isGrayScale:
            self.cv2Image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            self.lut = [0]*256
        else:
            self.cv2Image = cv2.imread(path, cv2.IMREAD_COLOR)
            self.cv2Image = cv2.cvtColor(self.cv2Image, cv2.COLOR_BGR2RGB)  # WAŻNE, BO CV2 DOMYŚLNIE ZAPISUJE W KOLEJNOŚĆ B, G, R
            self.lut = np.zeros(shape=(256, 3))

        self.name = path
        self.size = self.cv2Image.size
        self.fill_histogram()

    def check_if_is_gray(self):
        if len(self.cv2Image.shape) < 3: return True
        if self.cv2Image.shape[2]  == 1: return True
        b,g,r = self.cv2Image[:,:,0], self.cv2Image[:,:,1], self.cv2Image[:,:,2]
        if (b==g).all() and (b==r).all(): return True
        return False

    def fill_histogram(self):
        if self.isGrayScale:
            h, w = self.cv2Image.shape
            for i in range(h):
                for j in range(w):
                    self.lut[self.cv2Image[i][j]] += 1
        else:
            h, w, c = self.cv2Image.shape
            for i in range(h):
                for j in range(w):
                    for k in range(c):
                        self.lut[self.cv2Image[i][j][k], k] += 1        

        
