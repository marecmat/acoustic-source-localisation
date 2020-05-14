import numpy as np
import matplotlib.pyplot as plt
import TDOALocalisation

# np.random.randint(-100, 100)
capteurs = [
        (540, 850),
        (348, 23),
        (152, 350),
        ]
n = 1200 
mat = np.zeros((n, n))

for xs in range(n):
    print(xs)
    for ys in range(n):
        source_ac = (xs, ys)
        instance = TDOALocalisation.TDOALocalisation(source_ac, capteurs, T=15, step=1, max_dist=1500)
        data = instance.get_all_hyperboloid()
        try:
            x_inters, y_inters, mean = instance.intersection_estimation(data)
            xerr = abs(mean[0] - source_ac[0])
            yerr = abs(mean[1] - source_ac[1])
            derr = np.sqrt(xerr**2 + yerr**2)
            mat[xs, ys] = derr
        except IndexError:
            print("index error encountered at {}, {}".format(xs, ys)) 

np.savetxt("matrix_otherpos", mat, delimiter=",")
fig, ax = plt.subplots()
im = ax.pcolor(mat)
fig.colorbar(im)
ax.plot(*zip(*capteurs), 'mo', label='acoustic sensors')

ax.grid()
ax.legend()
ax.set_xlabel("X coordinates [m]")
ax.set_xlabel("Y coordinates [m]")
plt.show()
