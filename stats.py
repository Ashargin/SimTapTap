import matplotlib.pyplot as plt
import numpy as np

X = [-2.6, 7, 7, 7, 9, 10, 13, 18, 23, 26, 30, 9]
Y = [34804, 25612, 19821, 21682, 21088, 20791, 19900, 18415, 16930, 16039, 14851, 27606]
Z = [37960, 31608, 24462, 27002, 27002, 27002, 27002, 27002, 27002, 27002, 27002, 38882]
Y_reduction = [1 - Y[i] / Z[i] for i in range(len(Y))]

dmg_red = lambda x: (x + 11) / 91

Y_hyp = list(map(dmg_red, X))

plt.plot(X, Y_reduction, 'o')

X_func = np.linspace(-5, 30, 100)
Y_func = list(map(dmg_red, X_func))
plt.plot(X_func, Y_func)
plt.show()
