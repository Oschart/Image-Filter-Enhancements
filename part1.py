#%% 
import numpy as np
#import cv2
from skimage.io import imread, imshow
from parse_utils import trans_format
from parse_utils import parse_trans
from ImageTransformation import ImageTransformation
from ImageTransformer import ImageTransformer



#img_path = input(prompt="Insert image path")
img_path = 'he.jpg'
img = imread(img_path, as_gray=True)
#trans_str = input(prompt=trans_format)
trans_str = '''
<HE>
'''
ptrans = parse_trans(trans_str)
trans_list = []
for ptr in ptrans:
    trans = ImageTransformation(key=ptr[0], args=ptr[1])
    trans_list.append(trans)


transformer = ImageTransformer(tr_list=trans_list)

output = transformer.apply_all(img)
imshow(output)

# %%
