import numpy as np

def quadratic_interpolate(data_x, data_y, dx, x_test):
    ## it assumes linear distance between data in x axis (with the size of dx),
    ## and also assumes that data is sorted in ascending order of x.
    xt = np.copy(data_x)
    yt = np.copy(data_y)

    ng = len(xt)

    xmin = data_x[0]
    xt -= xmin

    g0 = np.int(np.floor((x_test - xmin) / dx + 0.5))
    gl = g0 - 1
    gr = g0 + 1

    g0 = max(g0, 0)
    g0 = min(g0, ng - 1)
    gl = max(gl, 0)
    gl = min(gl, ng - 1)
    gr = max(gr, 0)
    gr = min(gr, ng - 1)

    h = (x_test - xmin) / dx - g0
    f0 = 0.75 - h * h
    fl = 0.5 * (0.5 - h) * (0.5 - h)
    fr = 0.5 * (0.5 + h) * (0.5 + h)
    y = fl * data_y[gl] + f0 * data_y[g0] + fr * data_y[gr]

    df0 = - 2.0 / dx * h
    dfl = - (0.5 - h) / dx
    dfr = (0.5 + h) / dx

    grad_y = dfl * data_y[gl] + df0 * data_y[g0] + dfr * data_y[gr]

    return y, grad_y
