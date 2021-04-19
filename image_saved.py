import cv2
import numpy as np
import copy
import os

class ImageSaved():
    def __init__(self, path=None, imageArray=None):
        if path is not None:
            file_extension = os.path.splitext(path)[1]
            if file_extension == '.bmp':
                pass
                #OGARNIJ BMP
            #else do 20:

            self.cv2Image = cv2.imread(path, 1)
            self.isGrayScale = self.check_if_is_gray()
            if self.isGrayScale:
                self.cv2Image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            else:
                self.cv2Image = cv2.imread(path, cv2.IMREAD_COLOR)
                self.cv2Image = cv2.cvtColor(self.cv2Image, cv2.COLOR_BGR2RGB)  # WAŻNE, BO CV2 DOMYŚLNIE ZAPISUJE W KOLEJNOŚĆ B, G, R
        else:
            self.cv2Image = imageArray
            self.isGrayScale = self.check_if_is_gray()
            
        self.copy = copy.deepcopy(self.cv2Image)
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

    def equalize(self):
        if self.isGrayScale:
            cumulativeSum = self.lut.cumsum()    
            cumulativeSum = np.ma.masked_equal(cumulativeSum,0)
            minVal = cumulativeSum.min()
            maxVal = cumulativeSum.max()
            cumulativeSum = (((cumulativeSum-minVal)*255)/(maxVal - minVal)).astype(np.uint8)
            self.cv2Image = cumulativeSum[self.cv2Image]
        else:
            for canal in range(3):
                cumulativeSum = self.lut[:,canal].cumsum()
                cumulativeSum = np.ma.masked_equal(cumulativeSum,0)
                minVal = cumulativeSum.min()
                maxVal = cumulativeSum.max()
                cumulativeSum = (((cumulativeSum-minVal)*255)/(maxVal - minVal)).astype(np.uint8)
                self.cv2Image[:,canal] = cumulativeSum[self.cv2Image[:,canal]]

        self.copy = copy.deepcopy(self.cv2Image)
        self.fill_histogram()

    def stretch(self):
        minImg = np.amin(self.cv2Image)
        maxImg = np.amax(self.cv2Image)


        newMax = 255
        newMin = 0

        def calculate(oldPixel):
            return int(((oldPixel-minImg) * newMax)/(maxImg-minImg))

        func = np.vectorize(calculate)
        self.cv2Image = func(self.cv2Image)

        self.copy = copy.deepcopy(self.cv2Image)
        self.fill_histogram()

    def twoArgsOperations(self, operation, imgToAdd):
        img = imgToAdd.cv2Image
        img = cv2.resize(img, self.cv2Image.shape)

        operations = {
            "DODAJ": lambda:cv2.add(self.cv2Image, img),
            "ODEJMIJ": lambda:cv2.subtract(self.cv2Image, img),
            "ZMIESZAJ": lambda:cv2.addWeighted(self.cv2Image, 0.7, img, 0.5, -100),
            "AND": lambda:cv2.bitwise_and(self.cv2Image, img),
            "OR": lambda:cv2.bitwise_or(self.cv2Image, img),
            "XOR": lambda:cv2.bitwise_xor(self.cv2Image, img),
        }
        
        return operations[operation]()

    def neighborOperations(self, operation, borderPixels):

        operations = {
            "BLUR": lambda:cv2.blur(self.cv2Image, (5, 5), borderType=borderPixels),
            "GAUSSIAN": lambda:cv2.GaussianBlur(self.cv2Image, (5,5), 0, borderType=borderPixels),
            #"SOBEL": lambda:cv2.addWeighted(self.cv2Image, 0.7, img, 0.5, -100),
            #"LAPLASJAN": lambda:cv2.bitwise_and(self.cv2Image, img),
            #"CANNY": lambda:cv2.bitwise_or(self.cv2Image, img),
            #"PRW N": lambda:cv2.bitwise_xor(self.cv2Image, img),
            #"PRW NE": lambda:cv2.bitwise_xor(self.cv2Image, img),
            #"PRW E": lambda:cv2.bitwise_xor(self.cv2Image, img),
            #"PRW SE": lambda:cv2.bitwise_xor(self.cv2Image, img),
            #"PRW S": lambda:cv2.bitwise_xor(self.cv2Image, img),
            #"PRW SW": lambda:cv2.bitwise_xor(self.cv2Image, img),
            #"PRW W": lambda:cv2.bitwise_xor(self.cv2Image, img),
            #"PRW NW": lambda:cv2.bitwise_xor(self.cv2Image, img),
            #"LAPLASJAN 1": lambda:cv2.bitwise_and(self.cv2Image, img),
            #"LAPLASJAN 2": lambda:cv2.bitwise_and(self.cv2Image, img),
            #"LAPLASJAN 3": lambda:cv2.bitwise_and(self.cv2Image, img),
            #"MEDIAN 3": lambda:cv2.bitwise_and(self.cv2Image, img),
            #"MEDIAN 5": lambda:cv2.bitwise_and(self.cv2Image, img),
            #"MEDIAN 7": lambda:cv2.bitwise_and(self.cv2Image, img),
            #"CUSTOM": lambda:cv2.bitwise_and(self.cv2Image, img),
        }
        
        self.cv2Image = operations[operation]()
        self.fill_histogram()