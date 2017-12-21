import numpy as np
import PIL.Image

from guidedfilter import guidedfilter
from guidedfilter_color import guidedfilter_color


def enhancement():
    # example: detail enhancement
    # figure 6 in our paper
    I = np.asarray(PIL.Image.open('examples/tulips.png')) / 255
    p = I.copy()
    r = 16
    eps = 0.1**2
    q = np.zeros_like(I)
    q[:, :, 0] = guidedfilter(I[:, :, 0], p[:, :, 0], r, eps)
    q[:, :, 1] = guidedfilter(I[:, :, 1], p[:, :, 1], r, eps)
    q[:, :, 2] = guidedfilter(I[:, :, 2], p[:, :, 2], r, eps)
    I_enhanced = (I - q) * 5 + q
    I_enhanced = I_enhanced*255.
    I_enhanced = I_enhanced.astype('uint8')
    img = PIL.Image.fromarray(I_enhanced)
    img.save('examples/output/tulips.png')


def feathering():
    I = np.asarray(PIL.Image.open('examples/toy.png')) / 255
    p = np.asarray(PIL.Image.open('examples/toy-mask.png').convert('L')) / 255
    q = guidedfilter_color(I, p, r=60, eps=10**-6)
    imshow([I, np.repmat(p, [1, 1, 3]), np.repmat(q, [1, 1, 3])], [0, 1])
    return q


def flash():
    # example: flash/noflash denoising
    # figure 8 in our paper
    # *** Errata ***: there is a typo in the caption of figure 8, the eps should be 0.02^2 instead of 0.2^2 sig_r should be 0.02 instead of 0.2.
    I = np.asarray(PIL.Image.open('examples/cave-flash.png')) / 255
    p = np.asarray(PIL.Image.open('examples/cave-noflash.png')) / 255

    r = 8
    eps = 0.02**2
    q = np.zeros_like(I)

    q[:, :, 0] = guidedfilter(I[:, :, 0], p[:, :, 0], r, eps)
    q[:, :, 1] = guidedfilter(I[:, :, 1], p[:, :, 1], r, eps)
    q[:, :, 2] = guidedfilter(I[:, :, 2], p[:, :, 2], r, eps)
    q = q*255.
    q = q.astype('uint8')
    img = PIL.Image.fromarray(q)
    img.save('examples/output/cave.png')


def smoothing():
    # example: edge-preserving smoothing
    # figure 1 in our paper
    I = np.asarray(PIL.Image.open('examples/cat.png')) / 255
    p = I.copy()

    r = 4
    eps = 0.2**2
    q = np.zeros_like(I)

    q[:, :, 0] = guidedfilter(I[:, :, 0], p[:, :, 0], r, eps)
    q[:, :, 1] = guidedfilter(I[:, :, 1], p[:, :, 1], r, eps)
    q[:, :, 2] = guidedfilter(I[:, :, 2], p[:, :, 2], r, eps)
    q = q*255.
    q = q.astype('uint8')
    img = PIL.Image.fromarray(q)
    img.save('examples/output/cat.png')
