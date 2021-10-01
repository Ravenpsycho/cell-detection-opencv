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

    _, contours, hierarchy = cv2.findContours(th3, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    img_contours = cv2.drawContours(th3, contours, -1, (255, 0, 0))
    cv2.imshow('contours', img_contours)
    cv2.waitKey(0)

    size_list = np.array([cv2.contourArea(x) for x in contours])

    mean_size = size_list.mean()

    print(mean_size)
    contours_small = [x for x in contours if cv2.contourArea(x) <= 2000]

    img_contours2 = cv2.drawContours(th3, contours_small, -1, (255, 0, 0))

    cv2.imshow('th3', th3)
    cv2.waitKey(0)

    cv2.imshow('contours_2', img_contours2)
    cv2.waitKey(0)
