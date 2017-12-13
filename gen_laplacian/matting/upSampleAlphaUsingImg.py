import getLinearCoeff
import upSmpIm

def upSampleAlphaUsingImg(alpha, I, bI, varargin):
  
  coeff = getLinearCoeff(alpha,I,varargin{:})
  bcoeff = upSmpIm(coeff,[size(bI,1),size(bI,2)])
  balpha = bcoeff(:,:,end)
  for k=1:size(bI,3)
    balpha = balpha + bcoeff(:,:,k).*bI(:,:,k)
  return balpha
