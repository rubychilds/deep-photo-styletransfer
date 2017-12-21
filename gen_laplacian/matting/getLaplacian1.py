import numpy as np
import cv2
from scipy import sparse


def getLaplacian1(I, consts, epsilon=0.0000001, win_size=1):

  neb_size = (win_size*2 + 1)**2
  [h, w, c] = I.shape
  n = h
  m = w
  img_size = w * h
  consts = cv2.erode(consts, np.ones(win_size*2+1))

  indsM = np.arange(1, img_size+1).reshape((h,w))
  tlen = int(sum(sum(1-consts[win_size:-win_size, win_size:-win_size])) * (neb_size**2))

  row_inds = np.zeros((tlen, 1))
  col_inds = np.zeros((tlen, 1))
  vals = []
  length = 0
  for j in range(win_size, w-win_size):
    for i in range(win_size, h-win_size):
      if consts[i, j]:
        continue
      win_inds = indsM[i-win_size:i+win_size+1, j-win_size:j+win_size+1]
      win_inds = win_inds.flatten()
      winI = I[i-win_size:i+win_size+1, j-win_size:j+win_size+1,:]
      winI = winI.reshape((neb_size, c),order='F')/255.
      win_mu = np.transpose(np.mean(winI, 0))
      win_mu = win_mu.reshape((win_mu.shape[0], 1))

      win_var = np.linalg.inv(np.matmul(np.transpose(winI), winI)/neb_size - win_mu*np.transpose(win_mu) + epsilon/neb_size*np.identity(c))
      winI = winI - np.tile(np.transpose(win_mu), (neb_size, 1))
      tvals = (1 + np.matmul(np.matmul(winI, win_var), np.transpose(winI)))/neb_size

      row_inds[length:neb_size**2 + length] = np.reshape(np.tile(win_inds.reshape(win_inds.shape[0], 1), (1, neb_size)), (neb_size**2, 1))
      col_inds[length:neb_size**2 + length] = np.reshape(np.tile(np.transpose(win_inds.reshape(win_inds.shape[0], 1)), (neb_size, 1)), (neb_size**2, 1))
      tvals = tvals.flatten()
      vals += list(tvals)
      length = length + neb_size**2

  A = sparse.csr_matrix((np.array(vals), (row_inds, col_inds)), shape=(img_size, img_size))

  sumA = np.sum(A, 1)
  A = sparse.spdiags(sumA.flatten(), 0, img_size, img_size) - A

  return A1, A
