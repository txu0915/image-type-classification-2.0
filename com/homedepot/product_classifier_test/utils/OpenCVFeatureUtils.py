import numpy as np
import cv2
import imutils
import math
import operator

from collections import defaultdict
from PIL import Image
from skimage import feature, io, filters, measure
from scipy import ndimage
from scipy.stats import logistic, itemfreq

class OpenCVFeatureUtils:

    def __init__(self, feature_list, img_array):
        self.img_array = img_array
        self.feature_list = feature_list
        self.features = np.array([np.zeros(len(feature_list))])
        self.feature_maps = {
            "average_pixel_width": self.average_pixel_width,
            "touch_the_border": self.touch_the_border,
            "dark_pctg": self.perform_color_analysis,
            "rotation": self.rotation,
            "dominant_color": self.dominant_color,
            "number_of_object": self.number_of_object
        }

    def compute_feature(self):
        #print(self.feature_list)
        for i, f in enumerate(self.feature_list):
            self.features[0, i] = self.feature_maps[f]()
            #print(i,f,self.features)
        return self.features

    def average_pixel_width(self):
        im = Image.fromarray(self.img_array)
        im = np.asarray(im.convert(mode='L'))
        edges_sigma1 = feature.canny(im, sigma=3)
        apw = (float(np.sum(edges_sigma1)) / (self.img_array.shape[0] * self.img_array.shape[1]))
        return apw * 100

    def touch_the_border(self):
        gray = cv2.cvtColor(self.img_array, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, sqKernel)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        maxArea = 0.0
        i_max = 0
        if len(cnts) > 0:
            for i, c in enumerate(cnts):
                area = cv2.contourArea(c)
                if (area >= maxArea):
                    i_max = i
                    maxArea = area  ## new patch....
            (x, y, w, h) = cv2.boundingRect(cnts[i_max])
            if (x == 0 or y == 0 or x + w == self.img_array.shape[0] or y + h == self.img_array.shape[1]):
                return 1
        return 0

    def perform_color_analysis(self, flag='black'):
        def color_analysis(im):
            # obtain the color palatte of the image
            palatte = defaultdict(int)
            for pixel in im.getdata():
                palatte[pixel] += 1
            # sort the colors present in the image
            sorted_x = sorted(palatte.items(), key=operator.itemgetter(1), reverse=True)
            light_shade, dark_shade, shade_count, pixel_limit = 0, 0, 0, 25
            for i, x in enumerate(sorted_x[:pixel_limit]):
                if any(xx <= 60 for xx in x[0][:3]):  ## dull : too much darkness
                    dark_shade += x[1]
                if all(xx >= 240 for xx in x[0][:3]):  ## bright : too much whiteness
                    light_shade += x[1]
                shade_count += x[1]
            light_percent = round((float(light_shade) / shade_count) * 100, 2)
            dark_percent = round((float(dark_shade) / shade_count) * 100, 2)
            return light_percent, dark_percent

        im = Image.fromarray(self.img_array)
        im1 = im.crop((0, 0, self.img_array.shape[0], self.img_array.shape[1] / 2))
        im2 = im.crop((0, self.img_array.shape[1] / 2, self.img_array.shape[0], self.img_array.shape[1]))
        light_percent1, dark_percent1 = color_analysis(im1)
        light_percent2, dark_percent2 = color_analysis(im2)
        light_percent = (light_percent1 + light_percent2) / 2
        dark_percent = (dark_percent1 + dark_percent2) / 2
        if flag == 'black':
            return dark_percent
        return light_percent

    def rotation(self):
        img_gray = cv2.cvtColor(self.img_array, cv2.COLOR_BGR2GRAY)
        img_edges = cv2.Canny(img_gray, 100, 100, apertureSize=3)
        lines = cv2.HoughLinesP(img_edges, 1, math.pi / 180.0, 100, minLineLength=100, maxLineGap=5)
        if type(lines) == np.ndarray:
            angles = []
            for line in lines:
                for x1, y1, x2, y2 in line:
                    # cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
                    angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
                    angles.append(angle)
            # print(angles)
            median_angle = np.median(angles)
            if abs(median_angle) < 25:
                return median_angle
        # plt.imshow(img)
        return 0.0

    def dominant_color(self):
        arr = np.float32(self.img_array)
        pixels = arr.reshape((-1, 3))
        n_colors = 5
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
        flags = cv2.KMEANS_RANDOM_CENTERS
        _, labels, centroids = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
        palette = np.uint8(centroids)
        quantized = palette[labels.flatten()]
        quantized = quantized.reshape(np.shape(self.img_array))
        dominant_color = palette[np.argmax(itemfreq(labels)[:, -1])]
        #print("dominant color:",dominant_color)
        return np.mean(dominant_color)/255.

    def number_of_object(self):
        img_gray = cv2.cvtColor(self.img_array, cv2.COLOR_BGR2GRAY)
        val = filters.threshold_otsu(img_gray)
        # fill the holes of your binary image using ndimage.binary_fill_holes
        drops = ndimage.binary_fill_holes(img_gray < val)
        labels = measure.label(drops)
        return (labels.max())
