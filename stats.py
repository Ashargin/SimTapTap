import matplotlib.pyplot as plt
import numpy as np

X = [7, 9, 10, 13, 18, 23, 26, 30]
Y = [21682, 21088, 20791, 19900, 18415, 16930, 16039, 14851]
Y_reduction = [1 - Y[i] / 27002 for i in range(len(Y))]

plt.plot(X, Y_reduction, 'o')

X_func = np.linspace(-11, 80, 100)
Y_func = list(map(lambda x: (x + 11) / 91, X_func))
plt.plot(X_func, Y_func)
plt.show()
