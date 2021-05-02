import cv2
import numpy as np
import copy
import os
from filter_masks import mask_sharp1, mask_sharp2, mask_sharp3, mask_prewittNW, mask_prewittN, mask_prewittE, mask_prewittNE, mask_prewittS, mask_prewittSE, mask_prewittSW, mask_prewittW

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

    def check_if_binary(self):
        if not self.isGrayScale:
            print("Not gray")
            return False
        else:
            white_pix = np.sum(self.cv2Image == 255)
            black_pix = np.sum(self.cv2Image == 0)
            return self.cv2Image.shape[0]*self.cv2Image.shape[1] == white_pix+black_pix

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

        self.fill_histogram()

    def stretch(self, oldMin=None, oldMax=None, newMini=None, newMaxi=None):
        if all(v is None for v in (oldMin, oldMax, newMini, newMaxi)):
            minImg = np.amin(self.cv2Image)
            maxImg = np.amax(self.cv2Image)
            newMax = 255
            newMin = 0
        else:
            minImg = oldMin
            maxImg = oldMax
            newMax = newMaxi
            newMin = newMini

        def calculate(oldPixel):
            return int(((oldPixel-minImg) * newMax)/(maxImg-minImg))

        func = np.vectorize(calculate)
        self.cv2Image = np.where(np.logical_and(self.copy >= minImg, self.copy <= maxImg), func(self.cv2Image), self.copy) 
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

    def neighborOperations(self, operation, borderOption, customMask=None):
        outputType = cv2.CV_64F
        borderPixels = [cv2.BORDER_ISOLATED, cv2.BORDER_REFLECT, cv2.BORDER_REPLICATE][borderOption]

        operations = {
            "BLUR": lambda:cv2.blur(self.cv2Image, (5, 5), borderType=borderPixels),
            "GAUSSIAN": lambda:cv2.GaussianBlur(self.cv2Image, (5,5), 0, borderType=borderPixels),
            "SOBEL": lambda:self.handleSobel(outputType, borderPixels),
            "LAPLASJAN": lambda:self.normalize(cv2.Laplacian(self.cv2Image, outputType, ksize=3, borderType=borderPixels)),
            "CANNY": lambda:cv2.Canny(self.cv2Image, 100, 200),
            "PRW N": lambda:self.normalize(cv2.filter2D(self.cv2Image, outputType, mask_prewittN, borderType=borderPixels)),
            "PRW NE": lambda:self.normalize(cv2.filter2D(self.cv2Image, outputType, mask_prewittNE, borderType=borderPixels)),
            "PRW E": lambda:self.normalize(cv2.filter2D(self.cv2Image, outputType, mask_prewittE, borderType=borderPixels)),
            "PRW SE": lambda:self.normalize(cv2.filter2D(self.cv2Image, outputType, mask_prewittSE, borderType=borderPixels)),
            "PRW S": lambda:self.normalize(cv2.filter2D(self.cv2Image, outputType, mask_prewittS, borderType=borderPixels)),
            "PRW SW": lambda:self.normalize(cv2.filter2D(self.cv2Image, outputType, mask_prewittSW, borderType=borderPixels)),
            "PRW W": lambda:self.normalize(cv2.filter2D(self.cv2Image, outputType, mask_prewittW, borderType=borderPixels)),
            "PRW NW": lambda:self.normalize(cv2.filter2D(self.cv2Image, outputType, mask_prewittNW, borderType=borderPixels)),
            "LAPLASJAN 1": lambda:self.normalize(cv2.filter2D(self.cv2Image, outputType, mask_sharp1, borderType=borderPixels)), #BABOL?
            "LAPLASJAN 2": lambda:self.normalize(cv2.filter2D(self.cv2Image, outputType, mask_sharp2, borderType=borderPixels)), #BABOL?
            "LAPLASJAN 3": lambda:self.normalize(cv2.filter2D(self.cv2Image, outputType, mask_sharp3, borderType=borderPixels)), #BABOL?
            "MEDIAN 3": lambda:cv2.medianBlur(self.cv2Image, 3),
            "MEDIAN 5": lambda:cv2.medianBlur(self.cv2Image, 5),
            "MEDIAN 7": lambda:cv2.medianBlur(self.cv2Image, 7),
            "CUSTOM": lambda:self.normalize(cv2.filter2D(self.cv2Image, outputType, customMask, borderType=borderPixels)),
        }
        
        self.cv2Image = operations[operation]()
        self.fill_histogram()

    def handleSobel(self, dtype, borderPixels):
        sobelx = cv2.Sobel(self.cv2Image,dtype, 1,0,ksize=5, borderType=borderPixels)
        sobely = cv2.Sobel(self.cv2Image,dtype, 0,1,ksize=5, borderType=borderPixels)
        scaled_x = self.normalize(sobelx)
        scaled_y = self.normalize(sobely)
        return cv2.hconcat((scaled_x, scaled_y))

    def normalize(self, input):
        abs_input = np.absolute(input)
        scaled_input = np.uint8(255*abs_input/np.max(abs_input))
        return scaled_input

    def morphOperations(self, operation, shape, size, borderOption):
        kernel = np.ones((size, size), np.uint8) if shape=="KWADRAT" else np.uint8(np.add.outer(*[np.r_[:size//2,size//2:-1:-1]]*2)>=size//2)
        borderPixels = [cv2.BORDER_ISOLATED, cv2.BORDER_REFLECT, cv2.BORDER_REPLICATE][borderOption]
        operations = {
            "EROZJA": lambda: cv2.erode(self.cv2Image, kernel, iterations=2, borderType=borderPixels),
            "DYLACJA": lambda: cv2.dilate(self.cv2Image, kernel, iterations=2, borderType=borderPixels),
            "OTWARCIE": lambda: cv2.morphologyEx(self.cv2Image, cv2.MORPH_OPEN, kernel, iterations=2, borderType=borderPixels),
            "ZAMKNIĘCIE": lambda: cv2.morphologyEx(self.cv2Image, cv2.MORPH_CLOSE, kernel, iterations=2, borderType=borderPixels),
            "SZKIELETYZACJA": lambda: self.handleSkeletonize(borderPixels),
        }

        self.cv2Image = operations[operation]()
        self.fill_histogram()

    def handleSkeletonize(self, borderPixels):
        skel = np.zeros(self.cv2Image.shape, np.uint8)
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
        tmp_copy = copy.deepcopy(self.cv2Image)
        while True:
            im_open = cv2.morphologyEx(tmp_copy, cv2.MORPH_OPEN, kernel, borderType=borderPixels)
            im_temp = cv2.subtract(tmp_copy, im_open)
            im_eroded = cv2.erode(tmp_copy, kernel, borderType=borderPixels)
            skel = cv2.bitwise_or(skel,im_temp)
            tmp_copy = copy.deepcopy(im_eroded)
            if cv2.countNonZero(tmp_copy)==0:
                return skel