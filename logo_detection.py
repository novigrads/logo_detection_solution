import cv2
import numpy as np
import glob
import argparse
from utils import resize
from utils import crop_blackbg as crop

# hyperparams
root = '/Users/sileshu/Desktop/DriveInfromed/logo_detection/training_images/'
classes = ['Bank Of America', 'Wells Fargo', 'JPMorgan Chase', 'Citigroup Inc', 'Capital One', 'Other']
temp2class = {'BankOfAmerica.jpg':'Bank Of America', 
              'WellsFargo.jpg':'Wells Fargo', 
              'JPMorganChase.png':'JPMorgan Chase', 
              'Citigroup.jpg':'Citigroup Inc', 
              'CapitalOne.png':'Capital One'
             }

# build argument parser
ap = argparse.ArgumentParser()
ap.add_argument('image',action = 'store')
args = vars(ap.parse_args())

# load image to be classified
image = cv2.imread(root + args['image'],0)
edge = cv2.Canny(image, 50, 200)
iw,ih = edge.shape[:2]

maxi = None
res = None

for t in temp2class:
    # load each template
    template = cv2.imread(root + t,0)
    template = cv2.Canny(template, 50, 200)
    # crop the templates
    template = crop(template)
    w,h = template.shape[:2]
            
    for scale in np.linspace(.6, 3., 100)[::-1]:
        resized_template = resize(template, width = int(template.shape[1] * scale))
        tw,th = resized_template.shape[:2]
        if tw >= iw or th >= ih:
            continue
        result = cv2.matchTemplate(edge, resized_template, cv2.TM_CCORR_NORMED)
        minVal, maxVal, _, _ = cv2.minMaxLoc(result)
        
        
        if maxi is None or maxVal > maxi:
            maxi = maxVal
            res = t
            
if maxi > 0.4:
    print 'Document belongs to organization:' + '\"' + temp2class[res] + '\"'
else:
    print 'Document belongs to organization:' + '\"' + 'Other' + '\"'

