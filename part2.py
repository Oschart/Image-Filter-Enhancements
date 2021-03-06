# %%
import numpy as np
import time
from skimage.io import imread, imshow, show
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
import plotly.graph_objects as go

from parse_utils import trans_format, parse_trans, display_single_filter
from ImageTransformation import ImageTransformation
from ImageTransformer import ImageTransformer

F_id = np.array([
    [0, 0, 0],
    [0, 1, 0],
    [0, 0, 0]
])
F_smooth = np.ones(shape=(3, 3))/9.0

lap1 = np.array([
    [0, 1, 0],
    [1, -4, 1],
    [0, 1, 0]
])
lap2 = np.array([
    [1, 1, 1],
    [1, -8, 1],
    [1, 1, 1]
])
F_grad_lap = F_id - lap1
F_sharp = 2*F_id - F_smooth


def part_a():
    img_path = 'samples/smooth.jpg'
    img = imread(img_path, as_gray=True)

    transformer = ImageTransformer()

    # Smoothing filter:
    smooth_img = transformer.apply_filter(img, F_smooth)
    display_single_filter(img, smooth_img, effect_name="Smoothed")
    return


def part_b():
    img_path = 'samples/gradient.jpg'
    img = imread(img_path, as_gray=True)

    transformer = ImageTransformer()

    # Gradient filter:
    grad_img = transformer.apply_filter(img, lap2)
    graded_img = transformer.apply_filter(img, F_grad_lap)
    display_single_filter(
        img, graded_img, effect_name="Enhanced", grad=grad_img)
    return


def part_c():
    img_path = 'samples/sharpen.jpg'
    img = imread(img_path, as_gray=True)

    transformer = ImageTransformer()

    # Sharpening filter:
    sharpened_img = transformer.apply_filter(
        transformer.apply_filter(img, F_sharp), F_sharp)
    display_single_filter(img, sharpened_img, effect_name="Sharpened")
    return

# %%
