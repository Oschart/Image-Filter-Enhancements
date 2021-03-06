# %%
import numpy as np
import time
from skimage.io import imread, imshow, show
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.offline as pyo

from parse_utils import trans_format, parse_trans, display_single_filter
from ImageTransformation import ImageTransformation
from ImageTransformer import ImageTransformer


def display_decomp_res(imgs1D, imgs2D, sizes):
    n = len(sizes)
    fig, axes = plt.subplots(
        n, 2, sharex=True, sharey=True, figsize=(6, 6), dpi=100)
    
    fig.suptitle("2D Filters vs 1D Decomposition")
    
    for ax in axes.flat:
        ax.set(xticks=[], yticks=[])

    ax = axes.ravel()
    for i in range(0, 2*n, 2):
        k = sizes[i//2]
        ax[i].imshow(imgs2D[i//2], cmap='gray', aspect='auto')
        ax[i].get_xaxis().set_label_text(f"2D Filter ({k}x{k})")

        ax[i+1].imshow(imgs1D[i//2], cmap='gray', aspect='auto')
        ax[i+1].get_xaxis().set_label_text(f"1D Separated ({k}x{k})")
    plt.subplots_adjust(wspace=.05, hspace=.5)
    plt.show()


def display_time_plot(time_1d, time_2d, sizes):
    pyo.init_notebook_mode()
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
    pyo.iplot(fig, filename = 'basic-line')



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
    sizes = list(range(3, 16, 2))
    for _ in sizes[1:]:
        # 2D filter extension
        Fp = Fs_2D[-1]
        Fp = np.insert(Fp, (1, Fp.shape[0]-1), values=0, axis=0)
        Fp = np.insert(Fp, (1, 2), values=0, axis=1)
        Fs_2D.append(Fp)
        # 1D filter extension
        Fp_ = Fs_1D[-1]
        Fp_1 = np.insert(Fp_[0], (1, Fp_[0].shape[0]-1), values=0, axis=0)
        Fp_2 = np.insert(Fp_[1], (1, 2), values=0, axis=1)
        Fs_1D.append((Fp_1, Fp_2))


    img_path = 'samples/2d_decomp.jpg'
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
        img_i = transformer.apply_filter(
            img, Fs_1D[i][0], clip=False, padding='valid')
        img_f = transformer.apply_filter(
            img_i, Fs_1D[i][1], clip=True, padding='valid')
        end = time.time()
        time_1d.append(end-start)
        imgs_1d.append(img_f)

    # For 2D filters
    for i in range(len(sizes)):
        start = time.time()
        img_f = transformer.apply_filter(
            img, Fs_2D[i], clip=True, padding='valid')
        end = time.time()
        time_2d.append(end-start)
        imgs_2d.append(img_f)

    display_single_filter(imgs_1d[0],imgs_2d[0], orig_name="2D Filter (3x3)", effect_name="1D Separated")

    n2d = 4
    display_decomp_res(imgs_1d[:n2d], imgs_2d[:n2d], sizes[:n2d])
    display_time_plot(time_1d, time_2d, sizes)


#run()
# %%
