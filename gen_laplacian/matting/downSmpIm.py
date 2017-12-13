def downSmpIm(I, filtS=1):

    if filtS == 2:
      filt = [1,4,6,4,1] / 16
    if filtS == 1:
      filt = [1,2,1]/4

    for i=1:size(I,3):
      for j=1:size(I,4):
        I[:,:,i,j] = conv2(filt, 'filt', I(:,:,i,j),'same')

    return I(filtS+1:2:end-filtS,filtS+1:2:end-filtS[,:,:])
