import cv2
import numpy as np
import copy
import random
import os
from filter_masks import mask_sharp1, mask_sharp2, mask_sharp3, mask_prewittNW, mask_prewittN, mask_prewittE, mask_prewittNE, mask_prewittS, mask_prewittSE, mask_prewittSW, mask_prewittW

class ImageSaved():
    def __init__(self, path=None, imageArray=None):
        if path is not None:
            self.file_extension = os.path.splitext(path)[1]

            # Czytanie bmp...
            if self.file_extension == '.bmp':
                self.isGrayScale = True
                with open(path, 'rb') as bmp:
                    try:
                        signature = bmp.read(2).decode('utf-8')
                        if  signature == "BM": #Z jakiegoś powodu niektóre .bmp nie są prawdziwymi bmp
                            bmp.seek(10)
                            offset = int.from_bytes(bmp.read(4), 'little', signed=False)

                            bmp.seek(18)
                            bmp_w = int.from_bytes(bmp.read(4), 'little', signed=True)
                            bmp_h = int.from_bytes(bmp.read(4), 'little', signed=True)

                            bmp.seek(34, 0)
                            bmp_s = int.from_bytes(bmp.read(4), 'little', signed=False)

                            bmp.seek(28)
                            bpp = int.from_bytes(bmp.read(2), 'little', signed=False)

                            jumpVal = 1
                            if bpp == 24:
                                jumpVal = 3


                            if bmp_s == 0:
                                bmp_b = bmp_w
                            else:
                                bmp_b = int(bmp_s/bmp_h)
                                
                            bmp.seek(offset, 0)
                            bmp_line = []
                            bmp_whole = []
                            for _ in range(bmp_h):
                                for _ in range(bmp_b):
                                    bmp_byte = bmp.read(1)
                                    bmp_line.append((int.from_bytes(bmp_byte, 'little', signed=False)))
                                bmp_whole.append(bmp_line[:bmp_w if jumpVal == 1 else len(bmp_line):jumpVal])
                                bmp_line = []

                            bmp_whole.reverse()
                            reshaped = np.reshape(bmp_whole, (bmp_h,bmp_w))


                            self.cv2Image = np.uint8(reshaped)

                        else:
                            self.handle_not_bmp(path)
                    except UnicodeDecodeError:
                        self.handle_not_bmp(path)  
            else:
                self.handle_not_bmp(path)
        else:
            self.cv2Image = imageArray
            self.isGrayScale = self.check_if_is_gray()
            
        self.copy = copy.deepcopy(self.cv2Image)
        self.fill_histogram()

    def handle_not_bmp(self, path):
        self.cv2Image = cv2.imread(path, 1)
        self.isGrayScale = self.check_if_is_gray()
        if self.isGrayScale:
            self.cv2Image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        else:
            self.cv2Image = cv2.imread(path, cv2.IMREAD_COLOR)
            self.cv2Image = cv2.cvtColor(self.cv2Image, cv2.COLOR_BGR2RGB)  # WAŻNE, BO CV2 DOMYŚLNIE ZAPISUJE W KOLEJNOŚĆ B, G, R

    def check_if_is_gray(self):
        if len(self.cv2Image.shape) < 3: return True
        if self.cv2Image.shape[2]  == 1: return True
        b,g,r = self.cv2Image[:,:,0], self.cv2Image[:,:,1], self.cv2Image[:,:,2]
        if (b==g).all() and (b==r).all(): return True
        return False

    def check_if_binary(self):
        if not self.isGrayScale:
            return False
        else:
            white_pix = np.sum(self.cv2Image == 255)
            black_pix = np.sum(self.cv2Image == 0)
            return self.cv2Image.shape[0]*self.cv2Image.shape[1] == white_pix+black_pix

    def fill_histogram(self):
        if self.check_if_is_gray():
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

    def threshold_adapt(self, window_size):
        self.cv2Image = cv2.adaptiveThreshold(self.copy, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, window_size, 5)

    def threshold_otsu(self):
        blurred = cv2.GaussianBlur(self.cv2Image,(5,5),0)
        _, self.cv2Image = cv2.threshold(blurred,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        self.copy = copy.deepcopy(self.cv2Image)
        self.fill_histogram()

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

    def two_args_operations(self, operation, imgToAdd):
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

    def neighbor_operations(self, operation, borderOption, customMask=None):
        outputType = cv2.CV_64F
        borderPixels = [cv2.BORDER_ISOLATED, cv2.BORDER_REFLECT, cv2.BORDER_REPLICATE][borderOption]

        operations = {
            "BLUR": lambda:cv2.blur(self.cv2Image, (5, 5), borderType=borderPixels),
            "GAUSSIAN": lambda:cv2.GaussianBlur(self.cv2Image, (5,5), 0, borderType=borderPixels),
            "SOBEL": lambda:self.handle_sobel(outputType, borderPixels),
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

    def handle_sobel(self, dtype, borderPixels):
        sobelx = cv2.Sobel(self.cv2Image,dtype, 1,0,ksize=5, borderType=borderPixels)
        sobely = cv2.Sobel(self.cv2Image,dtype, 0,1,ksize=5, borderType=borderPixels)
        scaled_x = self.normalize(sobelx)
        scaled_y = self.normalize(sobely)
        return cv2.hconcat((scaled_x, scaled_y))

    def normalize(self, input):
        abs_input = np.absolute(input)
        scaled_input = np.uint8(255*abs_input/np.max(abs_input))
        return scaled_input

    def morph_operations(self, operation, shape, size, borderOption):
        kernel = np.ones((size, size), np.uint8) if shape=="KWADRAT" else np.uint8(np.add.outer(*[np.r_[:size//2,size//2:-1:-1]]*2)>=size//2)
        borderPixels = [cv2.BORDER_ISOLATED, cv2.BORDER_REFLECT, cv2.BORDER_REPLICATE][borderOption]
        operations = {
            "EROZJA": lambda: cv2.erode(self.cv2Image, kernel, iterations=2, borderType=borderPixels),
            "DYLACJA": lambda: cv2.dilate(self.cv2Image, kernel, iterations=2, borderType=borderPixels),
            "OTWARCIE": lambda: cv2.morphologyEx(self.cv2Image, cv2.MORPH_OPEN, kernel, iterations=2, borderType=borderPixels),
            "ZAMKNIĘCIE": lambda: cv2.morphologyEx(self.cv2Image, cv2.MORPH_CLOSE, kernel, iterations=2, borderType=borderPixels),
            "SZKIELETYZACJA": lambda: self.handle_skeletonize(borderPixels),
        }

        self.cv2Image = operations[operation]()
        self.fill_histogram()

    def handle_skeletonize(self, borderPixels):
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

    def my_watershed(self):
        if not self.isGrayScale: 
            self.cv2Image = cv2.cvtColor(self.cv2Image ,cv2.COLOR_BGR2GRAY)
        else:
            self.negate()

        _,self.cv2Image = cv2.threshold(self.cv2Image,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

        self.cv2Image = cv2.morphologyEx(self.cv2Image,cv2.MORPH_OPEN, np.ones((3,3),np.uint8), iterations = 1)

        sure_bg = cv2.dilate(self.cv2Image, np.ones((3,3),np.uint8),iterations=1)
        dist_transform = cv2.distanceTransform(self.cv2Image,cv2.DIST_L2,5)

        sure_fg = np.uint8(cv2.threshold(dist_transform,0.5*dist_transform.max(),255,0)[1])

        unknown = cv2.subtract(sure_bg,sure_fg)
        _, markers = cv2.connectedComponents(sure_fg)

        markers = markers+1
        markers[unknown==255] = 0

        if len(self.cv2Image.shape) == 2: 
            markers2 = cv2.watershed(cv2.merge((self.cv2Image,self.cv2Image,self.cv2Image)), markers)
        else:
            markers2 = cv2.watershed(self.cv2Image, markers)

        self.cv2Image[markers2 == -1] = 0
        #self.cv2Image = cv2.subtract(thresh, img_gray)
        #self.cv2Image[markers2 == -1] = 0

    def morph_line(self, horizontalW, horizontalH, veritcalW, verticalH,searchHorizontal, searchVertical, borderOption):
        horizontal = np.zeros_like(self.cv2Image)
        vertical = np.zeros_like(self.cv2Image)

        self.cv2Image = cv2.adaptiveThreshold(self.cv2Image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -2)

        if searchHorizontal:
            horizontal = self.handle_line_extraction(horizontalW, horizontalH, borderOption)

        if searchVertical:
            vertical = self.handle_line_extraction(verticalH, veritcalW, borderOption)

        self.cv2Image = cv2.add(horizontal, vertical)

    def handle_line_extraction(self, width, height, borderOption):
        output = np.copy(self.cv2Image)
        outputElement = cv2.getStructuringElement(cv2.MORPH_RECT, (width, height))
        output = cv2.erode(output, outputElement, borderType=borderOption)
        return cv2.dilate(output, outputElement, borderType=borderOption)

    def get_objects_vector(self):
        self.cv2Image = self.copy
        if not self.check_if_is_gray(): 
            self.cv2Image = cv2.cvtColor(self.cv2Image ,cv2.COLOR_BGR2GRAY)
        outerPoints = np.array([[[0,0]], [[0, self.cv2Image.shape[0]-1]], [[self.cv2Image.shape[1]-1, self.cv2Image.shape[0]-1]], [[self.cv2Image.shape[1]-1, 0]]])

        _,thresh = cv2.threshold(self.cv2Image,127,255,0)
        contours,hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.cv2Image = cv2.cvtColor(self.cv2Image, cv2.COLOR_GRAY2RGB)

        colours = []
        moments = []
        areas = []
        lengths = []
        aspectRatios = []
        extents = []
        solidities = []
        equivalentDiameters = []
        for cnt in contours:
            if len(cnt) == 4 and np.any(np.isin(outerPoints, cnt)):
                continue
            colour = random.randrange(50,250,25),random.randrange(50,250,25),random.randrange(50,250,25)
            cv2.drawContours(self.cv2Image, [cnt], 0, colour, 3)

            area = cv2.contourArea(cnt)
            _,_,w,h = cv2.boundingRect(cnt)
            rect_area = w*h
            hull = cv2.convexHull(cnt)
            hull_area = cv2.contourArea(hull)
            
            aspect_ratio = float(w)/h if h != 0 else 0
            extent = float(area)/rect_area if rect_area != 0 else 0
            solidity = float(area)/hull_area if hull_area != 0 else 0
            equi_diameter = np.sqrt(4*area/np.pi)

            colours.append(colour)
            moments.append(cv2.moments(cnt))
            areas.append(area)
            lengths.append(cv2.arcLength(cnt,True))
            aspectRatios.append(aspect_ratio)
            extents.append(extent)
            solidities.append(solidity)
            equivalentDiameters.append(equi_diameter)

        return colours, moments, areas, lengths, aspectRatios, extents, solidities, equivalentDiameters

    def get_objects_vector_img(self, image):
        outerPoints = np.array([[[0,0]], [[0, image.shape[0]-1]], [[image.shape[1]-1, image.shape[0]-1]], [[image.shape[1]-1, 0]]])
        _,thresh = cv2.threshold(image,127,255,0)
        contours,hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        moments = []
        areas = []
        lengths = []
        aspectRatios = []
        extents = []
        solidities = []
        equivalentDiameters = []
        for cnt in contours:
            if len(cnt) == 4 and np.any(np.isin(outerPoints, cnt)):
                continue

            area = cv2.contourArea(cnt)
            _,_,w,h = cv2.boundingRect(cnt)
            rect_area = w*h
            hull = cv2.convexHull(cnt)
            hull_area = cv2.contourArea(hull)
            
            aspect_ratio = float(w)/h if h != 0 else 0
            extent = float(area)/rect_area if rect_area != 0 else 0
            solidity = float(area)/hull_area if hull_area != 0 else 0
            equi_diameter = np.sqrt(4*area/np.pi)

            moments.append(cv2.moments(cnt))
            areas.append(area)
            lengths.append(cv2.arcLength(cnt,True))
            aspectRatios.append(aspect_ratio)
            extents.append(extent)
            solidities.append(solidity)
            equivalentDiameters.append(equi_diameter)

        return moments, areas, lengths, aspectRatios, extents, solidities, equivalentDiameters

    def classify(self):
        outerPoints = np.array([[[0,0]], [[0, self.cv2Image.shape[0]-1]], [[self.cv2Image.shape[1]-1, self.cv2Image.shape[0]-1]], [[self.cv2Image.shape[1]-1, 0]]])
        img1 = cv2.imread('train_imgs/train_ryz.jpg', cv2.IMREAD_GRAYSCALE)
        img2 = cv2.imread('train_imgs/train_soczewica.jpg', cv2.IMREAD_GRAYSCALE)
        img3 = cv2.imread('train_imgs/train_fasola.jpg', cv2.IMREAD_GRAYSCALE)
        feat1 = self.get_feat(self.get_objects_vector_img(img1))
        feat2 = self.get_feat(self.get_objects_vector_img(img2))
        feat3 = self.get_feat(self.get_objects_vector_img(img3))

        x_input = np.float32(np.concatenate((feat1,np.concatenate((feat2, feat3),axis =1)),axis =1).transpose())
        print(x_input.shape)
        t1 = self.get_target(feat1, 1)
        t2 = self.get_target(feat2, 2)
        t3 = self.get_target(feat3, 3)
        t_input = np.int64(np.concatenate((t1,np.concatenate((t2, t3)))))

        mysvm = cv2.ml.SVM_create()
        mysvm.setType(cv2.ml.SVM_C_SVC)
        mysvm.setKernel(cv2.ml.SVM_LINEAR)
        mysvm.setTermCriteria((cv2.TERM_CRITERIA_MAX_ITER, 10000, 1e-6))
        mysvm.train(x_input, cv2.ml.ROW_SAMPLE, t_input)

        if not self.check_if_is_gray(): 
            self.cv2Image = cv2.cvtColor(self.cv2Image ,cv2.COLOR_BGR2GRAY)
        feat_test = self.get_feat(self.get_objects_vector_img(self.cv2Image))
        _,thresh = cv2.threshold(self.cv2Image,127,255,0)
        contours,hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) 

        self.cv2Image = cv2.cvtColor(self.cv2Image,cv2.COLOR_GRAY2RGB)
        for x, cnt in enumerate(contours):
            if len(cnt) == 4 and np.any(np.isin(outerPoints, cnt)):
                continue
            sampleMat = np.float32(feat_test[:,x].reshape(-1,1).transpose())
            response = mysvm.predict(sampleMat)[1]
            if response == 1:
                cv2.drawContours(self.cv2Image, [cnt], 0, (0,255,0), 3) # zielony = ryz
            elif response == 2:
                cv2.drawContours(self.cv2Image, [cnt], 0, (255,0,0), 3) # niebieski = soczewica
            elif response == 3:
                cv2.drawContours(self.cv2Image, [cnt], 0, (0,0,255), 3) # czerwony = fasola
            else:
                cv2.drawContours(self.cv2Image, [cnt], 0, (255,255,255), 3)


    def get_feat(self, vector):
        M, area, perimeter, aspect_ratio, extent, solidities, equi_diameter = vector
        
        M_vec = np.array([np.array(list(m.values())) for m in M])
        M_vec.reshape(-1,1)
        M_vec = np.hstack((M_vec, np.array(area).reshape(-1,1)))
        M_vec = np.hstack((M_vec, np.array(perimeter).reshape(-1,1)))
        M_vec = np.hstack((M_vec, np.array(aspect_ratio).reshape(-1,1)))
        M_vec = np.hstack((M_vec, np.array(extent).reshape(-1,1)))
        M_vec = np.hstack((M_vec, np.array(solidities).reshape(-1,1)))
        M_vec = np.hstack((M_vec, np.array(equi_diameter).reshape(-1,1))).transpose()

        return M_vec

    def get_target(self,input_feats, target_class = 1):
        sh = input_feats.shape
        out = np.ones((sh[1],1))
        return out*target_class