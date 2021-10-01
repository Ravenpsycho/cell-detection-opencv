# Project aim

Trying to detect identify cell location through DAPI staining (nuclei) and use detected area to quantify staining in another 
color.

The challenge is to find the right parameters for the functions `GaussianBlur`, `treshold` and `SimpleBlobDetector`, all
part of the `open_cv` package.

## GaussianBlur:

|Parameter      |Description    |
| ------------- |---------------|
|src	        |input image    |
|dst            |output image   |
|ksize          |Gaussian Kernel Size. [height width]. height and width should be odd and can have different values. If ksize is set to [0 0], then ksize is computed from sigma values.|
|sigmaX         |Kernel standard deviation along X-axis (horizontal direction).|
|sigmaY         |Kernel standard deviation along Y-axis (vertical direction). If sigmaY=0, then sigmaX value is taken for sigmaY
|borderType     |Specifies image boundaries while kernel is applied on image borders. Possible values are : cv.BORDER_CONSTANT cv.BORDER_REPLICATE cv.BORDER_REFLECT cv.BORDER_WRAP cv.BORDER_REFLECT_101 cv.BORDER_TRANSPARENT cv.BORDER_REFLECT101 cv.BORDER_DEFAULT cv.BORDER_ISOLATED