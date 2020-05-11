import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('error_test.txt', skiprows=1, delimiter=' ')
source_ac = (-17.5684651, 42.375784874)

error = data[:, 0]
x = data[:, 1]
y = data[:, 2]
distance = np.sqrt((x - source_ac[0])**2 + (y - source_ac[1])**2)
print(distance)
fig, ax = plt.subplots()
ax.plot(error, distance, 'bo')
ax.set_xlabel(r"Error $\Delta t$ on the time delay measurement [s]")
ax.set_ylabel(r"Distance to the source [m]")
plt.show()