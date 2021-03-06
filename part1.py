# %%
import matplotlib.pyplot as plt
import numpy as np
#import cv2
from skimage.io import imread, imshow

from ImageTransformation import ImageTransformation
from ImageTransformer import ImageTransformer
from parse_utils import display_single_filter, parse_trans, trans_format


def run(interactive=True, img_path='samples/rome.jpg', trans_str='', effect='', aspect='equal', side_by_side=True):
    if interactive:
        img_path = input("Insert image path")
        trans_str = input(trans_format)

    img = imread(img_path, as_gray=True)

    ptrans = parse_trans(trans_str)
    trans_list = []
    for ptr in ptrans:
        trans = ImageTransformation(key=ptr[0], args=ptr[1])
        trans_list.append(trans)

    transformer = ImageTransformer(tr_list=trans_list)

    output = transformer.apply_all(img)
    if side_by_side:
        display_single_filter(img, output, effect_name=effect, aspect=aspect)
    else:
        plt.imshow(img, cmap='gray')
        plt.title('Original Image')
        plt.show()
        plt.imshow(output, cmap='gray')
        plt.title(effect)
        plt.show()
