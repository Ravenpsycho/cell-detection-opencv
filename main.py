import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # load
    img = cv2.imread('data/img/dapi.TIF')
    img2 = cv2.imread('data/img/android_motherboard-2048x1536.jpg')
    cv2.imshow('original image', img)
    cv2.waitKey(0)
    # Convert to graycsale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    # Blur the image for better edge detection
    blur = cv2.GaussianBlur(img_gray, (5, 5), cv2.BORDER_DEFAULT)

    cv2.imshow('blurred image', blur)
    cv2.waitKey(0)

    ret3, th3 = cv2.threshold(blur, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    cv2.imshow('th3', th3)
    cv2.waitKey(0)

    cv2.imshow('OTSU', cv2.bitwise_and(th3, img2_gray))
    cv2.waitKey(0)
