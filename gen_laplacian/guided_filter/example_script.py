import numpy as np
import PIL.Image
import guildedfilter
import guidedfilter_color



def enhancement():
    # example: detail enhancement
    # figure 6 in our paper

    I = double(imread('examples/tulips.bmp')) / 255
    p = I

    r = 16
    eps = 0.1**2

    q = np.zeros_like(I)

    q[:, :, 0] = guidedfilter(I[:, :, 0], p[:, :, 0], r, eps)
    q[:, :, 1] = guidedfilter(I[:, :, 1], p[:, :, 1], r, eps)
    q[:, :, 2] = guidedfilter(I[:, :, 2], p[:, :, 2], r, eps)

    I_enhanced = (I - q) * 5 + q
    return I_enhanced


def feathering():
    I = double(imread('.\img_feathering\toy.bmp')) / 255
    p = double(rgb2gray(imread('.\img_feathering\toy-mask.bmp'))) / 255

    r = 60
    eps = 10**-6

    q = guidedfilter_color(I, p, r, eps)

    imshow([I, np.repmat(p, [1, 1, 3]), np.repmat(q, [1, 1, 3])], [0, 1])
    return q


def flash():
    # example: flash/noflash denoising
    # figure 8 in our paper
    # *** Errata ***: there is a typo in the caption of figure 8, the eps should be 0.02^2 instead of 0.2^2 sig_r should be 0.02 instead of 0.2.

    I = double(imread('.\img_flash\cave-flash.bmp')) / 255
    p = double(imread('.\img_flash\cave-noflash.bmp')) / 255

    r = 8
    eps = 0.02**2
    q = np.zeros_like(I)

    q(:, :, 1) = guidedfilter(I(:, :, 1), p(:, :, 1), r, eps)
    q(:, :, 2) = guidedfilter(I(:, :, 2), p(:, :, 2), r, eps)
    q(:, :, 3) = guidedfilter(I(:, :, 3), p(:, :, 3), r, eps)

    imshow([I, p, q], [0, 1])


def smoothing():
    # example: edge-preserving smoothing
    # figure 1 in our paper

    I = double(imread('.\img_smoothing\cat.bmp')) / 255
    p = I
    r = 4 # try r=2, 4, or 8
    eps = 0.2**2 # try eps=0.1^2, 0.2^2, 0.4^2

    q = guidedfilter(I, p, r, eps)

    imshow([I, q], [0, 1])
