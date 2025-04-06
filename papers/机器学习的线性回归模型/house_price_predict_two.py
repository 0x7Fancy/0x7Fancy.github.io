import numpy as np

X1 = np.array([1985, 1534, 1427, 1380, 1494])
X2 = np.array([4, 3, 3, 3, 3])
Y = np.array([299.900, 314.900, 198.999, 212.000, 242.500])

x1 = np.sum(X1) / X1.size
x2 = np.sum(X2) / X2.size
y = np.sum(Y) / Y.size
print("bar_x1 = {0}".format(x1))
print("bar_x2 = {0}".format(x2))
print("bar_y = {0}".format(y))

x1y = np.sum(np.multiply(X1, Y)) / Y.size
x2y = np.sum(np.multiply(X2, Y)) / Y.size
x1x1 = np.sum(np.multiply(X1, X1)) / Y.size
x1x2 = np.sum(np.multiply(X1, X2)) / Y.size
x2x2 = np.sum(np.multiply(X2, X2)) / Y.size
print("bar_x1y = {0}".format(x1y))
print("bar_x2y = {0}".format(x2y))
print("bar_x1x1 = {0}".format(x1x1))
print("bar_x1x2 = {0}".format(x1x2))
print("bar_x2x2 = {0}".format(x2x2))

w1 = ((x1y-x1*y)*(x2x2-x2**2) - (x2y-x2*y)*(x1x2-x1*x2)) / ((x1x1-x1**2)*(x2x2-x2**2) - (x1x2-x1*x2)**2)
w2 = ((x1y-x1*y)*(x1x2-x1*x2) - (x2y-x2*y)*(x1x1-x1**2)) / ((x1x2-x1*x2)**2 - (x2x2-x2**2)*(x1x1-x1**2))
b = y - w1*x1 - w2*x2
print("w1 = {0}".format(w1))
print("w2 = {0}".format(w2))
print("b = {0}".format(b))
