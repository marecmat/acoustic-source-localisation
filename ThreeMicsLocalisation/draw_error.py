import numpy as np
import matplotlib.pyplot as plt
import TDOALocalisation
import datetime

# np.random.randint(-100, 100)
capteurs = [
        (84, 173),
        (18, 25),
        (166, 108),
        ]
n = 200
mat = np.zeros((n, n))

for xs in range(n):
    print(xs)
    for ys in range(n):
        source_ac = (xs, ys)
        instance = TDOALocalisation.TDOALocalisation(source_ac, capteurs, T=15, step=1, max_dist=600)
        data = instance.get_all_hyperboloid()
        try:
            x_inters, y_inters, mean = instance.intersection_estimation(data)
            xerr = abs(mean[0] - source_ac[0])
            yerr = abs(mean[1] - source_ac[1])
            derr = np.sqrt(xerr**2 + yerr**2)
            mat[xs, ys] = derr
        except IndexError:
            print("index error encountered at {}, {}".format(xs, ys)) 

timestamp = datetime.datetime.now()
np.savetxt("matrix_otherpos_{}".format(timestamp), mat, delimiter=",")
mat = np.nan_to_num(mat)
mat = np.array(mat)

xmax, xmin = mat.max(), mat.min()
mat = (mat - xmin) / (xmax - xmin)
print(mat)
mat[mat == 0] = np.nan

fig, ax = plt.subplots()

im = ax.pcolor(mat)
cb = fig.colorbar(im)
cb.set_label('Normalized deviation')
ax.plot(*zip(*capteurs), 'mo', label='acoustic sensors')

ax.grid()
ax.legend()
ax.set_xlabel("X coordinates [m]")
ax.set_xlabel("Y coordinates [m]")
plt.show()
