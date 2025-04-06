import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection='3d')

X = np.array([1985, 1534, 1427, 1380, 1494])
Y = np.array([4, 3, 3, 3, 3])
Z = np.array([299.900, 314.900, 198.999, 212.000, 242.500])
ax.scatter(X, Y, Z, c='red')

X, Y = np.meshgrid(X, Y)
Z = 0.654*X - 286.37*Y + 147.180
ax.plot_surface(X, Y, Z)

plt.show()
