import getLaplacian1
import numpy as np


def solveAlpha(I, consts_map1, consts_vals1, varargin):

  [h,w,c] = I.shape
  img_size = w*h
  A = getLaplacian1(I, consts_map, varargin{:})

  D = spdiags(consts_map(:),0,img_size,img_size)
  lambda_ = 100
  x = (A + lambda_* D) / (lambda_ * consts_map1(:). * consts_vals1(:))

  alpha = max(min(np.reshape(x,(h,w)),1),0)
  return alpha
