import numpy as np


def boxfilter(imSrc, r):

    #   BOXFILTER   O(1) time box filtering using cumulative sum
    #
    #   - Definition imDst(x, y) = sum(sum(imSrc(x-r:x+r,y-r:y+r)))
    #   - Running time independent of r
    #   - Equivalent to the function: colfilt(imSrc, [2*r+1, 2*r+1], 'sliding', @sum)
    #   - But much faster.

    [rows, cols] = imSrc.shape
    imDst = np.zeros_like(imSrc)

    # cumulative sum over Y axis
    imCum = np.cumsum(imSrc, 0)
    # difference over Y axis
    imDst[0:r+1, :] = imCum[r:2*r+1, :]
    imDst[r+1:rows-r, :] = imCum[2*r+1:rows, :] - imCum[0:rows-2*r-1, :]
    imDst[rows-r:rows, :] = np.tile(imCum[rows-1, :], [r, 1]) - imCum[rows-2*r-1:rows-r-1, :]

    # cumulative sum over X axis
    imCum = np.cumsum(imDst, 1)
    # difference over Y axis
    imDst[:, 0:r+1] = imCum[:, r:2*r+1]
    imDst[:, r+1:cols-r] = imCum[:, 2*r+1:cols] - imCum[:, 0:cols-2*r-1]
    imDst[:, cols-r:cols] = np.tile(imCum[:, cols-1], [r, 1]).T - imCum[:, cols-2*r-1:cols-r-1]
    return imDst
