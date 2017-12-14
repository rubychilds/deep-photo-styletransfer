import numpy as np
import cv2


def getLaplacian1(I, consts, epsilon=0.0000001, win_size=1):

  neb_size = (win_size*2 + 1)**2
  [h, w, c] = I.shape
  n = h
  m = w
  img_size = w * h
  consts = cv2.erode(consts, np.ones(win_size*2+1))

  indsM = np.arange(1, img_size+1).reshape((w,h))
  tlen = int(sum(sum(1-consts[win_size:-win_size, win_size:-win_size])) * (neb_size**2))

  row_inds = np.zeros((tlen, 1))
  col_inds = np.zeros((tlen, 1))
  vals = np.zeros((tlen, 1))
  length = 0
  for j in range(win_size, w-win_size-1):
    for i in range(win_size, h-win_size-1):
      if consts[i,j]:
        continue
      win_inds = indsM[i-win_size:i+win_size+1, j-win_size:j+win_size+1]
      win_inds = win_inds.flatten()
      winI = I[i-win_size:i+win_size+1, j-win_size:j+win_size+1,:]
      winI = winI.reshape((neb_size, c))
      win_mu = np.transpose(np.mean(winI, 0))
      win_mu = win_mu.reshape((win_mu.shape[0], 1))

      win_var = np.linalg.inv(np.matmul(np.transpose(winI/255.), winI/255.)/neb_size - win_mu/255.*np.transpose(win_mu/255.) + epsilon/neb_size*np.identity(c))

      winI = winI/255. - np.tile(np.transpose(win_mu/255.), (neb_size, 1))

      tvals = (1 + np.matmul(np.matmul(winI, win_var),np.transpose(winI)))/neb_size

      row_inds[length:neb_size**2 + length] = np.reshape(np.tile(win_inds.reshape(win_inds.shape[0], 1), (1, neb_size)), (neb_size**2, 1))
      col_inds[length:neb_size**2 + length] = np.reshape(np.tile(np.transpose(win_inds.reshape(win_inds.shape[0], 1)), (neb_size, 1)), (neb_size**2, 1))
      tvals = tvals.flatten()
      vals[length:neb_size**2 + length] = np.reshape(tvals, (tvals.shape[0], 1))
      length = length + neb_size**2

  vals = vals(1:length)
  row_inds=row_inds(1:length)
  col_inds=col_inds(1:length)
  A=sparse(row_inds,col_inds,vals,img_size,img_size)

  sumA = sum(A,2)
  A = spdiags(sumA(:),0,img_size,img_size)-A

  return A1, A
