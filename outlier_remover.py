import cv2
import numpy as np
import pandas as pd
import re

from errorHandling.Errors import DirNotMatchingError, ListLengthError, MisMatchError, MissingValueError
from os import listdir
from os.path import isfile, join, split
from pathlib import Path
from tkinter.filedialog import askdirectory


class OutlierRemover:
    def __init__(self, factor=10, score=True, verbose=False):
        self.factor = factor
        self.score = score
        self.verbose = verbose

        self.dir = None
        self.pat_dapi = None
        self.pat_other = None
        self.list_dapi = []
        self.list_other = []
        self.score_df = pd.DataFrame(columns=['file', 'dapi_score', f'{self.pat_other}_score'])

    def set_labels(self, dapi_label, other_label):
        self.pat_dapi = dapi_label
        self.pat_other = other_label

    def set_dir(self):
        self.dir = askdirectory(title='Select a Folder', initialdir='.')

    def get_dir(self):
        return self.dir

    def get_lists(self, short=False):
        if short:
            list_dapi = [split(x)[1] for x in self.list_dapi]
            list_other = [split(x)[1] for x in self.list_other]
            return [list_dapi, list_other]
        return [self.list_dapi, self.list_other]

    def get_labels(self):
        return [self.pat_dapi, self.pat_other]

    def remove_outliers(self, dapi_url, other_channel_url):
        # split path and set dir
        dapi_path = split(dapi_url)
        other_path = split(other_channel_url)

        if dapi_path[0] != other_path[0]:
            raise DirNotMatchingError('The directories of the files do not match')

        # setup dir
        output_dir = dapi_path[0] + '/outliers_removed'
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # load both images
        img = cv2.imread(dapi_url)
        img2 = cv2.imread(other_channel_url)

        # show
        if self.verbose:
            cv2.imshow('original image DAPI', img)
            cv2.waitKey(0)
            cv2.imshow('original image to apply mask on', img2)
            cv2.waitKey(0)

        # Convert to grayscale
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Blur the image for better edge detection
        blur = cv2.GaussianBlur(img_gray, (5, 5), cv2.BORDER_DEFAULT)
        if self.verbose:
            cv2.imshow('blurred image', blur)
            cv2.waitKey(0)

        # use threshold to have a 1_0 cut between edges and background
        ret3, th3 = cv2.threshold(blur, 200, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        if self.verbose:
            cv2.imshow('th3', th3)
            cv2.waitKey(0)

        # use findContours to delimit the shapes, also allows to have the size of the contours
        _, contours, hierarchy = cv2.findContours(image=th3, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
        plot_img = img.copy()

        # OPTIONAL: plot using drawContours on a copy of the original image
        cv2.drawContours(plot_img, contours, contourIdx=-1, color=(0, 255, 0),
                         thickness=3, lineType=cv2.FILLED)
        if self.verbose:
            cv2.imshow('contours of ALL structures', plot_img)
            cv2.waitKey(0)

        # the size is captured in an array using contourArea and list comprehension
        size_list = np.array([cv2.contourArea(x) for x in contours])
        # we can then request the mean
        mean_size = size_list.mean()

        # setting a cutoff at 10 times the mean gets rid of the problematic structures,
        # we only keep those in a list
        contours_big = [x for x in contours if cv2.contourArea(x) >= self.factor * mean_size]

        # again, plotting the big structures using drawContours
        plot_img = img.copy()
        cv2.drawContours(plot_img, contours_big, -1, (0, 255, 0), 3, cv2.LINE_AA)
        if self.verbose:
            cv2.imshow('contours of big structures', plot_img)
            cv2.waitKey(0)

        # initializing a full white mask (255 values across a np array the same size as our image)
        mask = np.zeros(img.shape, np.uint8) + 255

        # setting the shapes of the big structures to zero
        cv2.drawContours(mask, contours_big, -1, 0, -1)

        # applying the mask on the second picture
        mask_applied = cv2.bitwise_and(mask, img2)
        if self.verbose:
            cv2.imshow('mask applied', mask_applied)
            cv2.waitKey(0)

        # output in the subdir
        m = re.match(r'(.*)(\..*)', other_path[1])
        filepath = output_dir + "/" + m.group(1) + f'_outliers_removed_({len(contours_big)})' + m.group(2)
        cv2.imwrite(filepath, mask_applied)

        print(mean_size)

        # output the scoring
        if self.score:
            score_other_img = cv2.cvtColor(mask_applied, cv2.COLOR_BGR2GRAY)
            score_dapi_img = cv2.cvtColor(cv2.bitwise_and(mask, img), cv2.COLOR_BGR2GRAY)
            dapi_values = [score_dapi_img[i, j]
                           for i in range(score_dapi_img.shape[0])
                           for j in range(score_dapi_img.shape[1])
                           ]
            other_values = [score_other_img[i, j]
                            for i in range(score_other_img.shape[0])
                            for j in range(score_other_img.shape[1])
                            ]

            self.score_df = self.score_df.append({
                'file': other_path[1],
                'dapi_score': np.array(dapi_values).mean(),
                f'{self.pat_other}_score': np.array(other_values).mean()
            }, ignore_index=True)

    def find_matches(self):
        if self.pat_dapi == '' or self.pat_other == '':
            raise MissingValueError('One of the pattern values is missing')

        if self.pat_dapi == self.pat_other:
            raise ValueError('The values for dapi and other cannot be identical')

        self.list_dapi = []
        self.list_other = []
        only_files = [f for f in listdir(self.dir) if isfile(join(self.dir, f))]
        dapi_matches = [re.match(r".*" + self.pat_dapi + r".*\..*", x) for x in only_files]
        other_matches = [re.match(r".*" + self.pat_other + r".*\..*", x) for x in only_files]
        dapi_files = [x.group(0) for x in dapi_matches if x is not None]
        other_files = [x.group(0) for x in other_matches if x is not None]

        test_dapi = [x.replace(self.pat_dapi, '') for x in dapi_files]
        test_other = [x.replace(self.pat_other, '') for x in other_files]

        if len(test_dapi) != len(test_other):
            raise ListLengthError(f' The Dapi list is not the same length as the {self.pat_other} list')

        if dapi_files == other_files:
            raise ValueError('Chosen expressions return the same list!')

        for i in range(len(test_dapi)):
            if test_dapi[i] != test_other[i]:
                raise MisMatchError(f'The lists (dapi, {self.pat_other}) are the same' +
                                    'length but the rest of their names do not match')

        self.list_dapi += [self.dir + "/" + f for f in dapi_files]
        self.list_other += [self.dir + "/" + f for f in other_files]

    def run(self):
        for i in range(len(self.list_dapi)):
            print(f'processing image {i} of {len(self.list_dapi)}')
            self.remove_outliers(self.list_dapi[i], self.list_other[i])

        if self.score:
            self.score_df.to_csv("{0}/outliers_removed/scoring.csv".format(self.dir))


if __name__ == '__main__':
    outlier_finder = OutlierRemover()
    outlier_finder.set_labels('d1', 'd0')
    outlier_finder.find_matches()
    outlier_finder.run()
