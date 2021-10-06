import cv2
import numpy as np
import os.path
import re

from pathlib import Path
from errorHandling.Errors import DirNotMatchingError


def remove_dapi_outliers(dapi_url, other_channel_url):

    # split path and set dir
    dapi_path = os.path.split(dapi_url)
    other_path = os.path.split(other_channel_url)

    if dapi_path[0] != other_path[0]:
        raise DirNotMatchingError('The directories of the files do not match')

    # setup dir
    output_dir = dapi_path[0] + '/outliers_removed'
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # load both images
    img = cv2.imread(dapi_url)
    img2 = cv2.imread(other_channel_url)

    # show
    cv2.imshow('original image DAPI', img)
    cv2.waitKey(0)
    cv2.imshow('original image to apply mask on', img2)
    cv2.waitKey(0)

    # Convert to grayscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Blur the image for better edge detection
    blur = cv2.GaussianBlur(img_gray, (5, 5), cv2.BORDER_DEFAULT)
    cv2.imshow('blurred image', blur)
    cv2.waitKey(0)

    # use threshold to have a 1_0 cut between edges and background
    ret3, th3 = cv2.threshold(blur, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imshow('th3', th3)
    cv2.waitKey(0)

    # use findContours to delimit the shapes, also allows to have the size of the contours
    _, contours, hierarchy = cv2.findContours(image=th3, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
    plot_img = img.copy()

    # OPTIONAL: plot using drawContours on a copy of the original image
    cv2.drawContours(plot_img, contours, contourIdx=-1, color=(0, 255, 0),
                     thickness=3, lineType=cv2.FILLED)
    cv2.imshow('contours of ALL structures', plot_img)
    cv2.waitKey(0)

    # the size is captured in an array using contourArea and list comprehension
    size_list = np.array([cv2.contourArea(x) for x in contours])
    # we can then request the mean
    mean_size = size_list.mean()

    # setting a cutoff at 10 times the mean gets rid of the problematic structures,
    # we only keep those in a list
    contours_big = [x for x in contours if cv2.contourArea(x) >= 10*mean_size]

    # again, plotting the big structures using drawContours
    plot_img = img.copy()
    cv2.drawContours(plot_img, contours_big, -1, (0, 255, 0), 3, cv2.LINE_AA)
    cv2.imshow('contours of big structures', plot_img)
    cv2.waitKey(0)

    # initializing a full white mask (255 values across a np array the same size as our image)
    mask = np.zeros(img.shape, np.uint8) + 255

    # setting the shapes of the big structures to zero
    cv2.drawContours(mask, contours_big, -1, 0, -1)

    # applying the mask on the second picture
    mask_applied = cv2.bitwise_and(mask, img2)
    cv2.imshow('mask applied', mask_applied)
    cv2.waitKey(0)

    # output in the subdir
    m = re.match(r'(.*)(\..*)', other_path[1])
    filepath = output_dir + "/" + m.group(1) + '_outliers_removed' + m.group(2)
    cv2.imwrite(filepath, mask_applied)


if __name__ == '__main__':
    remove_dapi_outliers('data/img/dapi.TIF', 'data/img/android_motherboard-2048x1536.jpg')

