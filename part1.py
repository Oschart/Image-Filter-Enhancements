#%%
import numpy as np
#import cv2
from skimage.io import imread, imshow
from parse_utils import trans_format
from parse_utils import parse_trans
from ImageTransformation import ImageTransformation


#img_path = input(prompt="Insert image path")
img_path = 'rome.jpg'
img = imread(img_path, as_gray=True)
#trans_str = input(prompt=trans_format)
trans_str = '<ROT 0.5 0 0>'
ptrans = parse_trans(trans_str)
trans1 = ptrans[0][0]
args = ptrans[0][1]
trans = ImageTransformation(trans1, args)
output = trans.apply(img)
imshow(output)

# %%
