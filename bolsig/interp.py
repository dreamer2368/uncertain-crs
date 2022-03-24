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

def histogram_weight_2d(data_x, data_y, Nx, Ny, xlim, ylim):
    Np = len(data_x)
    xmin, xmax = xlim
    ymin, ymax = ylim

    dx, dy = (xmax - xmin) / (Nx + 1), (ymax - ymin) / (Nx + 1)

    gxl = (np.floor((data_x - xmin) / dx)).astype(np.int)
    gxr = gxl + 1
    hx = (data_x - xmin) / dx - gxl
    fxl = 1.0 - hx
    fxr = hx

    gyl = (np.floor((data_y - ymin) / dy)).astype(np.int)
    gyr = gyl + 1
    hy = (data_y - ymin) / dy - gyl
    fyl = 1.0 - hy
    fyr = hy

    wg = np.zeros([Nx+1, Ny+1])
    for p in range(Np):
        if( (gxl[p]<0) or (gxr[p]>Nx) or (gyl[p]<0) or (gyr[p]>Ny) ): continue

        wg[gxl[p], gyl[p]] += fxl[p] * fyl[p] / Np
        wg[gxl[p], gyr[p]] += fxl[p] * fyr[p] / Np
        wg[gxr[p], gyl[p]] += fxr[p] * fyl[p] / Np
        wg[gxl[p], gyr[p]] += fxr[p] * fyr[p] / Np

    data_w = np.zeros((Np,))
    for p in range(Np):
        if( (gxl[p]<0) or (gxr[p]>Nx) or (gyl[p]<0) or (gyr[p]>Ny) ): continue

        data_w[p] += fxl[p] * fyl[p] * wg[gxl[p], gyl[p]]
        data_w[p] += fxr[p] * fyl[p] * wg[gxr[p], gyl[p]]
        data_w[p] += fxl[p] * fyr[p] * wg[gxl[p], gyr[p]]
        data_w[p] += fxr[p] * fyr[p] * wg[gxr[p], gyr[p]]

    return data_w
