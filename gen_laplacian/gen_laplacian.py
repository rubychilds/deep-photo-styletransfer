import numpy as np
import PIL.Image

from gen_laplacian.reshape_img import reshape_img
import gen_laplacian.matting.getLaplacian1
import gen_laplacian.gaimc.sparse_to_csr


for i in range(1, 61):
    in_name = 'examples/input/in%d.png' %i
    img = PIL.Image.open(in_name)
    img = reshape_img(img, 700)
    img = np.asarray(img)
    [h, w, c] = img.shape

    A = getLaplacian1(img, np.zeros((h, w)), 1e-7, 1)

    n = np.count_nonzero(A)
    [Ai, Aj, Aval] = np.nonzero(A > 0)
    CSC = [Ai, Aj, Aval]
    save(['Input_Laplacian_3x3_1e-7_CSC%d.mat' %i], 'CSC')

    [rp, ci, ai] = sparse_to_csr(A)
    Ai = sort(Ai)
    Aj = ci
    Aval = ai
    CSR = [Ai, Aj, Aval]
    save(['Input_Laplacian_3x3_1e-7_CSR%d.mat' %i], 'CSR')
