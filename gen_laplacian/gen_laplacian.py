import reshape_img
import matting.getLaplacian1
import numpy as np
import PIL.Image


for i in range(1, 61):
    in_name = '../examples/input/in%d.png' %i
    img = PIL.Image.open(in_name)
    img.thumbnail((700,700))
    img = np.asarray(img)
    [h, w, c] = img.shape

    A = getLaplacian1(img, np.zeros((h, w)), 1e-7, 1)

    n = nnz(A)
    [Ai, Aj, Aval] = find(A)
    CSC = [Ai, Aj, Aval]
    save(['Input_Laplacian_3x3_1e-7_CSC' int2str(i) '.mat'], 'CSC')

    [rp ci ai] = sparse_to_csr(A)
    Ai = sort(Ai)
    Aj = ci
    Aval = ai
    CSR = [Ai, Aj, Aval]
    save(['Input_Laplacian_3x3_1e-7_CSR' int2str(i) '.mat'], 'CSR')
