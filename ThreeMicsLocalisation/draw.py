import numpy as np
import matplotlib.pyplot as plt
import TDOALocalisation

# np.random.randint(-100, 100)
source_ac = (-17.5, 42.37)
capteurs = [
        (540, 850),
        (348, 23),
        (152, 350),
        ]
error_range = 5e-1

# Creating the class instance
instance = TDOALocalisation.TDOALocalisation(source_ac, capteurs, T=15, step=0.5, max_dist=300, time_noise=200000)
# PARAB contains a list of hyperbola equations
data = instance.get_all_hyperboloid()

x_inters, y_inters, mean = instance.intersection_estimation(data)
print("calculated source position is at: x={:.3f}, y={:.3f}".format(mean[0], mean[1]))
print("actual source is at: x={:.3f}, y={:.3f}".format(source_ac[0], source_ac[1]))


fig, ax = plt.subplots()
ax.plot(*source_ac, 'k^', label="acoustic source")
ax.plot(*zip(*capteurs), 'mo', label='acoustic sensors')

for i in range(len(x_inters)):
    if i == 0:
        ax.plot(x_inters[0][:], y_inters[0][:], 'bo', alpha=0.3, label='calculated source position')
    else:
        ax.plot(x_inters[i][:], y_inters[i][:], 'bo', alpha=0.3)

for p in data:
    p = zip(*p)
    ax.plot(*p, '--', label='Curve computed')

ax.grid()
ax.legend()
ax.set_xlabel("X coordinates [m]")
ax.set_xlabel("Y coordinates [m]")
plt.show()
