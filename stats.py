import matplotlib.pyplot as plt
import numpy as np

saw = [(27002, 7, 21682), (27002, 9, 21088), (27002, 10, 20791), (27002, 13, 19900), (27002, 18, 18415), (27002, 23, 16930), (27002, 26, 16039), (27002, 30, 14851)]
medusa = [(32612, 10, 25110), (32612, 30, 17936), (32612, 22, 20806), (32612, 9, 25469), (32612, 20, 21523), (32612, 35, 16142), (32612, 7, 26187)]
freya = [(17098, 10, 13165), (17098, 22, 10908), (17098, 23, 10720), (17098, 20, 11284), (17098, 26, 10156), (17098, 35, 8463), (17098, 18, 11660), (17098, 9, 13353), (17098, 7, 13729), (17098, 30, 9403)]
devalys = [(37530, 8, 26820), (37530, 10, 26075), (37530, 11, 25702), (37530, 12, 25330), (37530, 20, 22350), (37530, 22, 21605), (37530, 23, 21232), (37530, 26, 20115)]

dmg_red = lambda x: x * 0.01099986 + 0.12002754658928322
dmg_red_devalys = lambda x: x * 0.00992543 + 0.20597124
X_func = np.linspace(-5, 40, 100)
Y_func = list(map(dmg_red, X_func))
colors = ['blue', 'orange', 'red', 'green']
for i, data in enumerate([saw, medusa, freya, devalys]):
    plt.figure()
    dmg, X, Y = zip(*data)
    Y_reduction = [1 - Y[i] / dmg[i] for i in range(len(Y))]
    plt.plot(X, Y_reduction, 'o', c=colors[i])
    plt.plot(X_func, Y_func, c='black')

plt.show()
