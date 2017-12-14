import guidedfilter_color


def refine_posterization(I, J):
    r = 8
    eps = 0.1**2
    I_f = I.copy()
    for c in range(1,3):
        I_f[:, :, c] = guidedfilter_color(I, I_f[:, :, c], r, eps)
    return J + I - I_f
