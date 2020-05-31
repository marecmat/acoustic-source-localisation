import numpy as np
import matplotlib.pyplot as plt

xs = [
    [50, 100, 150], 
    [50, 150, 100],
    [50, 100, 150], 
    [50, 100, 125], 
    [75, 140, 150],
    [69, 64, 160],
    [106, 80, 166],
    [84, 18, 162]
]

ys = [
    [75, 100, 125], 
    [50, 50, 150], 
    [100, 100, 100],
    [50, 100, 125], 
    [80, 70, 175], 
    [92, 61, 31], 
    [143, 43, 108],
    [173, 25, 87]
]

fig, axes = plt.subplots(4, 2, figsize=(8.27, 11.69))
for n, ax in enumerate(axes.flat):
    n = n + 1 

    data = np.loadtxt('data_{}'.format(n), delimiter=',')
    data = np.nan_to_num(data)
    data = data.transpose()
    xmax, xmin = data.max(), data.min()
    data = (data - xmin) / (xmax - xmin)
    data[data == 0] = np.nan

    im = ax.pcolor(data)
    ax.plot(xs[n-1], ys[n-1], 'mo')
    points = [(i, j) for i, j in zip(xs[n-1], ys[n-1])]
    ax.set_title("{}) {}".format(n, points))

fig.subplots_adjust(right=0.9)
cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
cbar = fig.colorbar(im, cax=cbar_ax)
cbar.set_label("Normalized deviation")
fig.tight_layout=True
plt.show()
