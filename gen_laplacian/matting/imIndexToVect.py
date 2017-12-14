import numpy as np


def imIndexToVect(Y, X, imHeight):
    return np.reshape(Y + (X-1)*imHeight, (prod(X.shape), 1))
