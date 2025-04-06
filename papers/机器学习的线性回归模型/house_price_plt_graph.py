import numpy as np
import matplotlib.pyplot as plt

plt.xlim(0, 3500)
plt.ylim(0, 600)

X = np.array([[2104, 399.900], [1600, 329.900], [2400, 369.000], [1416, 232.000], [3000, 539.900]])
plt.scatter(X[:,0], X[:,1])
plt.xlabel("size in feet2")
plt.ylabel("price in $1000's")

x = np.linspace(150, 3300)
y = 0.165 * x + 26.781
plt.plot(x, y, "-")

x = np.linspace(150, 2500)
y = 0.165 * x + 150
plt.plot(x, y, "--")

x = np.linspace(150, 3300)
y = 0.10 * x + 50
plt.plot(x, y, "--")

plt.show()
