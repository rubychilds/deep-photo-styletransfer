def reshape_img(im, length, nargin=2):
    if nargin < 2:
        length = 512

    [h, w, ~] = im.shape
    if h > w:
        h2 = length
        w2 = floor(w * h2 / h)
    else:
        w2 = length
        h2 = floor(h * w2 / w);

    return imresize(im, [h2 w2])
