# %%
import numpy as np
import time
from skimage.io import imread, imshow, show
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from parse_utils import trans_format
from parse_utils import parse_trans
from ImageTransformation import ImageTransformation
from ImageTransformer import ImageTransformer


def display_decomp_res(imgs1D, imgs2D, sizes):
    n = len(sizes)
    fig, axes = plt.subplots(2, n, sharex=True, sharey=True)
    
    ax = axes.ravel()
    for i in range(n):
        k = sizes[i]
        ax[i].set_title(f"{k}x{k} Original")
        ax[i].imshow(imgs2D[i], cmap='gray')
        ax[i+n].set_title(f"{k}x{k} Decomposed")
        ax[i+n].imshow(imgs1D[i], cmap='gray')
    plt.show()


def display_time_plot(time_1d, time_2d, sizes):
    fig = go.Figure(data=go.Scatter(
        x=sizes,
        y=time_1d,
        name="1D Filters time"
    ))

    fig.add_trace(go.Scatter(
        x=sizes,
        y=time_2d,
        name="2D Filter time"
    ))

    fig.update_layout(
        title_text='Execution time: 2D Filter vs 1D Decomposed Filters',
        title_x=0.5,
        yaxis_title="Time (s)",
        xaxis_title="Filter Size (WxW)"
    )
    #fig.write_html('%s/%s_interactive.html' % (plot_dir, fname))
    #fig.show()


def run():
    F = np.array([
        [1, 0, -1],
        [2, 0, -2],
        [1, 0, -1]
    ])
    F1 = np.array([1, 2, 1]).reshape(3, 1)
    F2 = np.array([1, 0, -1]).reshape(1, 3)

    Fs_2D = [F]
    Fs_1D = [(F1, F2)]
    sizes = [3, 5, 7, 11]
    for _ in sizes[1:]:
        # 2D filter extension
        Fp = Fs_2D[-1]
        Fp = np.insert(Fp, (1, Fp.shape[0]-3), values=0, axis=0)
        Fp = np.insert(Fp, (1, 2), values=0, axis=1)
        Fs_2D.append(Fp)
        # 1D filter extension
        Fp_ = Fs_1D[-1]
        Fp_1 = np.insert(Fp_[0], (1, Fp.shape[0]-3), values=0, axis=0)
        Fp_2 = np.insert(Fp_[1], (1, 2), values=0, axis=1)
        Fs_1D.append((Fp_1, Fp_2))

    img_path = 'samples/2d_decomp2.jpg'
    img = imread(img_path, as_gray=True)
    plt.imshow(img, cmap='gray')
    plt.title('Original Image')
    plt.show()
    transformer = ImageTransformer()

    time_1d, time_2d = [], []
    imgs_1d, imgs_2d = [], []
    # For 1D filters
    for i in range(len(sizes)):
        start = time.time()
        img_i = transformer.apply_filter(img, Fs_1D[i][0])
        img_f = transformer.apply_filter(img_i, Fs_1D[i][1])
        end = time.time()
        time_1d.append(end-start)
        imgs_1d.append(img_f)

    # For 2D filters
    for i in range(len(sizes)):
        start = time.time()
        img_f = transformer.apply_filter(img, Fs_2D[i])
        end = time.time()
        time_2d.append(end-start)
        imgs_2d.append(img_f)

    display_decomp_res(imgs_1d, imgs_2d, sizes)
    display_time_plot(time_1d, time_2d, sizes)


run()
# %%
