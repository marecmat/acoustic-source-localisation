import numpy as np
import matplotlib.pyplot as plt
import datetime

stamp = datetime.datetime.now()
print(stamp)

data = np.loadtxt('matrix_otherpos', delimiter=',')
print(data, data.shape)
data = np.array(data)

fig, ax = plt.subplots(2, 1)

im0 = ax[0].pcolor(data)
cb0 = fig.colorbar(im0)
cb0.set_label("Normalized deviation")

data = np.nan_to_num(data)
xmax, xmin = data.max(), data.min()
print(xmax, xmin)
data = (data - xmin) / (xmax - xmin)
data[data == 0] = np.nan
im1 = ax[1].pcolor(data)
cb1 = fig.colorbar(im1)
cb1.set_label("Normalized deviation")

plt.show()
