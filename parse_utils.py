# %%
import re

import matplotlib.pyplot as plt

trans_format = '''
Please insert a list of your transformations in the following format:
<trans_key1 ...args1> <trans_key2 ...args2> ... <trans_key_n ...args_n> 

Available transormations:
<TRANS offset>
<SCALE Sx Sy>
<ROT angle(degrees) Px Py>
<NTHP n>
<HE>
'''


def parse_trans(trans_str):
    ptrans = re.findall(r'\<(.*?)\>', trans_str)
    sep_trans = []
    for trans in ptrans:
        sp = trans.split(' ')
        sep_trans.append([sp[0], [float(st) for st in sp[1:]]])
    return sep_trans


def display_single_filter(img_orig, img_filt, orig_name="Original", effect_name=None, aspect='equal', grad=None):
    if grad is None:
        n = 2
        w = 5
    else:
        n = 3
        w = 8
    fig, axes = plt.subplots(
        1, n, sharex=True, sharey=True, figsize=(8, w), dpi=100)
    # fig.suptitle(filter_name)
    axes[0].set_title(orig_name,
                      fontdict=None, loc='center', color="k")
    axes[0].imshow(img_orig, cmap='gray', aspect=aspect)
    axes[0].get_xaxis().set_visible(False)
    axes[0].get_yaxis().set_visible(False)

    axes[1].set_title(effect_name,
                      fontdict=None, loc='center', color="k")
    axes[1].imshow(img_filt, cmap='gray', aspect=aspect)
    axes[1].get_xaxis().set_visible(False)
    axes[1].get_yaxis().set_visible(False)

    if n == 3:
        axes[2].set_title('Gradient',
                          fontdict=None, loc='center', color="k")
        axes[2].imshow(grad, cmap='gray', aspect=aspect)
        axes[2].get_xaxis().set_visible(False)
        axes[2].get_yaxis().set_visible(False)

    for ax in axes:
        ax.label_outer()
    plt.show()
# %%
