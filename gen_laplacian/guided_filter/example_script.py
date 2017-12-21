import numpy as np
import PIL.Image

import guildedfilter
import guidedfilter_color


def enhancement():
    # example: detail enhancement
    # figure 6 in our paper
    I = np.asarray(PIL.Image.open('examples/tulips.bmp')) / 255
    p = I
    r = 16
    eps = 0.1**2
    q = np.zeros_like(I)
    q[:, :, 0] = guidedfilter(I[:, :, 0], p[:, :, 0], r, eps)
    q[:, :, 1] = guidedfilter(I[:, :, 1], p[:, :, 1], r, eps)
    q[:, :, 2] = guidedfilter(I[:, :, 2], p[:, :, 2], r, eps)
    I_enhanced = (I - q) * 5 + q
    img = PIL.Image.fromarray(q*255)
    img.save('examples/output/tulips.png')


def feathering():
    I = np.asarray(PIL.Image.open('examples/toy.bmp')) / 255
    p = np.asarray(PIL.Image.open('examples/toy-mask.bmp').convert('L')) / 255
    q = guidedfilter_color(I, p, r=60, eps=10**-6)
    imshow([I, np.repmat(p, [1, 1, 3]), np.repmat(q, [1, 1, 3])], [0, 1])
    return q


def flash():
    # example: flash/noflash denoising
    # figure 8 in our paper
    # *** Errata ***: there is a typo in the caption of figure 8, the eps should be 0.02^2 instead of 0.2^2 sig_r should be 0.02 instead of 0.2.
    I = np.asarray(PIL.Image.open('examples/cave-flash.bmp')) / 255
    p = np.asarray(PIL.Image.open('examples/cave-noflash.bmp')) / 255

    r = 8
    eps = 0.02**2
    q = np.zeros_like(I)

    q[:, :, 0] = guidedfilter(I[:, :, 0], p[:, :, 0], r, eps)
    q[:, :, 1] = guidedfilter(I[:, :, 1], p[:, :, 1], r, eps)
    q[:, :, 2] = guidedfilter(I[:, :, 2], p[:, :, 2], r, eps)

    img = PIL.Image.fromarray(q*255)
    img.save('examples/output/cave.png')


def smoothing():
    # example: edge-preserving smoothing
    # figure 1 in our paper
    I = np.asarray(PIL.Image.open('examples/cat.bmp')) / 255
    p = I.copy()
    q = guidedfilter(I, p, r=4, eps=0.2**2)
    img = PIL.Image.fromarray(q*255)
    img.save('examples/output/cat.png')
