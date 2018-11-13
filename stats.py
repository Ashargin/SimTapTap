import matplotlib.pyplot as plt

X = [0, 7, 9, 10, 13, 18, 23, 26, 30]
Y = [27002, 21682, 21088, 20791, 19900, 18415, 16930, 16039, 14851]
Y_reduction = [1 - Y[i] / Y[0] for i in range(len(Y))]

plt.plot(X, Y_reduction, 'o')
plt.show()
