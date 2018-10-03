import numpy as np
import cv2

def resize(image, width = None, height = None, inter = cv2.INTER_AREA):
	dim = None
	(h, w) = image.shape[:2]

	if width is None and height is None:
		return image

	if width is None:
		r = height / float(h)
		dim = (int(w * r), height)
	else:
		r = width / float(w)
		dim = (width, int(h * r))
	resized = cv2.resize(image, dim, interpolation = inter)
	return resized
    
def crop_blackbg(image):
    w,h = image.shape[:2]
    edges_x = []
    edges_y = []
    for i in range(w):
        for j in range(h):
            if image[i][j] == 255:
                edges_x.append(i)
                edges_y.append(j)
    left = min(edges_x)
    right  = max(edges_x)
    top = max(edges_y)
    bottom = min(edges_y)
    width = right - left
    height = top - bottom
    return image[left:left+width,bottom:bottom+height]