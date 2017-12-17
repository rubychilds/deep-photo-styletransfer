import PIL.Image
import math


def reshape_img(im, length, nargin=2):
    if nargin < 2:
        length = 512

    w, h = im.size
    if h > w:
        h2 = length
        w2 = math.floor(w * h2 / h)
    else:
        w2 = length
        h2 = math.floor(h * w2 / w);
    return im.resize((w2, h2))
