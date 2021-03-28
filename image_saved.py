import cv2
import numpy as np
import copy

class ImageSaved():
    def __init__(self, path):
        self.cv2Image = cv2.imread(path, 1)
        self.isGrayScale = self.check_if_is_gray()
        if self.isGrayScale:
            self.cv2Image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        else:
            self.cv2Image = cv2.imread(path, cv2.IMREAD_COLOR)
            self.cv2Image = cv2.cvtColor(self.cv2Image, cv2.COLOR_BGR2RGB)  # WAŻNE, BO CV2 DOMYŚLNIE ZAPISUJE W KOLEJNOŚĆ B, G, R
            

        self.copy = copy.deepcopy(self.cv2Image)
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
            self.lut = np.zeros(shape=256).astype(int)
            h, w = self.cv2Image.shape
            for i in range(h):
                for j in range(w):
                    self.lut[self.cv2Image[i][j]] += 1
        else:
            self.lut = np.zeros(shape=(256, 3)).astype(int)
            h, w, c = self.cv2Image.shape
            for i in range(h):
                for j in range(w):
                    for k in range(c):
                        self.lut[self.cv2Image[i][j][k], k] += 1        

    def negate(self):
        maxVal = np.amax(self.cv2Image)
        self.cv2Image = maxVal - self.cv2Image
        self.copy = copy.deepcopy(self.cv2Image)
        self.fill_histogram()

    def threshold(self, level, keep_val):
        currCopy = copy.deepcopy(self.copy)
        if keep_val:
            self.cv2Image = np.where(currCopy <= level, 0, self.copy).astype(np.uint8)

        else:
            self.cv2Image = np.where(currCopy <= level, 0, 255).astype(np.uint8)

    def posterize(self, numOfBins):
        currCopy = copy.deepcopy(self.copy)
        binArray = np.arange(np.round(255/numOfBins), 255, np.round(255/numOfBins))

        self.cv2Image[currCopy <= binArray[0]] = 0
        pointer = 0
        for bin in binArray[1:]:
            self.cv2Image[np.logical_and(currCopy > binArray[pointer], currCopy <= bin)] = binArray[pointer]
            pointer += 1

        self.cv2Image[currCopy > binArray[-1]] = 255
        