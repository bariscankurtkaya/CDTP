import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt


def edgeDetection(img):
    edges = cv.Canny(img, 100, 200)
    plt.subplot(121), plt.imshow(img, cmap='gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(edges, cmap='gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    plt.show()


imgList = ['./Dataset/1.jpg','./Dataset/2.jpg','./Dataset/3.jpg','./Dataset/4.jpg','./Dataset/5.jpg','./Dataset/6.jpg']

for i in range(len(imgList)):
    img = cv.imread(imgList[i], 0)
    edgeDetection(img)

