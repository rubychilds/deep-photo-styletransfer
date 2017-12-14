import numpy as np


def getLinearCoeff(alpha, I, epsilon=0.0000001, win_size=1):

  neb_size = (win_size*2+1)**2
  [h, w, c] = I.shape
  n = h
  m = w
  img_size = w*h

  indsM = np.reshape([1:img_size],(h,w))
  coeff = np.zeros(h,w,c+1)

  for j=1+win_size:w-win_size:
    for i=win_size+1:h-win_size:

      win_inds = indsM[i-win_size:i+win_size, j-win_size:j+win_size]
      win_inds = win_inds.flatten()
      winI = I[i-win_size:i+win_size, j-win_size:j+win_size,:]
      winI = np.reshape(winI,(neb_size, c))

      G = [[winI, np.ones((neb_size,1))], [np.identity(c)*epsilon^0.5, np.zeros((c,1))]]

      tcoeff = inv(np.transpose(G)*G)*np.transpose(G)*[alpha(win_inds), np.zeros((c, 1))]
      coeff[i,j,:] = np.reshape(tcoeff, (1, 1, c+1_)

  coeff[1:win_size,:,:] = np.tile(coeff(win_size+1,:,:),(win_size, 1)_
  coeff[end-win_size+1:end,:,:] = np.tile(coeff(end-win_size,:,:), (win_size, 1))
  coeff[:,1:win_size,:] = np.tile(coeff(:,win_size+1,:), (1, win_size))
  coeff[:,end-win_size+1:end,:] = np.tile(coeff(:,end-win_size,:),(1, win_size))

  return coeff
