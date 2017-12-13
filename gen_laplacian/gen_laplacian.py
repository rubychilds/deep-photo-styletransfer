import reshape_img
import getLaplacian1
import numpy as np
import PIL


for i in range(1,60):
    prefix = '../examples/input/'
    in_name = [prefix 'in' int2str(i) '.png']
    disp(['Working on image index = ' int2str(i)])

    img = im2double(imread(in_name))
    img = reshape_img(img, 700)
    img.shape

    [h w c] = img.shape

    disp('Compute Laplacian')
    A = getLaplacian1(input, zeros(h, w), 1e-7, 1)

    disp('Save to disk')
    n = nnz(A);
    [Ai, Aj, Aval] = find(A)
    CSC = [Ai, Aj, Aval]
    save(['Input_Laplacian_3x3_1e-7_CSC' int2str(i) '.mat'], 'CSC')

    [rp ci ai] = sparse_to_csr(A)
    Ai = sort(Ai)
    Aj = ci
    Aval = ai
    CSR = [Ai, Aj, Aval]
    save(['Input_Laplacian_3x3_1e-7_CSR' int2str(i) '.mat'], 'CSR')
