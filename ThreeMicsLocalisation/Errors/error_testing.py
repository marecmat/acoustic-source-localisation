import numpy as np
import matplotlib.pyplot as plt
import TDOALocalisation

# np.random.randint(-100, 100)
source_ac = (-17.5684651, 42.375784874)
capteurs = [
        (-100, 50),
        (200, -57),
        (650, 347),
        (np.random.randint(-100, 100), np.random.randint(-200, 200)),
        (np.random.randint(-100, 100), np.random.randint(-100, 100)),
        ]

error_range = 5e-1
print("Error value X_position Y_position")
for i in range(3000):
    # Creating the class instance
    instance = TDOALocalisation.TDOALocalisation(source_ac, capteurs, error=error_range, T=15, step=0.5, max_dist=300)
    # PARAB contains a list of parabola equations
    PARAB = instance.get_all_paraboloid()
    error = instance.get_error()

    x_inters, y_inters, mean = instance.intersection_estimation(PARAB)
    print(error, mean[0], mean[1])