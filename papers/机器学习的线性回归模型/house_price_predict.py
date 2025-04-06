import numpy as np

X = np.array([2104, 1600, 2400, 1416, 3000])
Y = np.array([399.900, 329.900, 369.000, 232.000, 539.900])

bar_x = np.sum(X) / X.size
bar_y = np.sum(Y) / Y.size
print("bar_x = {0}".format(bar_x))
print("bar_y = {0}".format(bar_y))

bar_xx = np.sum(np.multiply(X, X)) / X.size
bar_yy = np.sum(np.multiply(Y, Y)) / X.size
bar_xy = np.sum(np.multiply(X, Y)) / X.size
print("bar_xx = {0}".format(bar_xx))
print("bar_yy = {0}".format(bar_yy))
print("bar_xy = {0}".format(bar_xy))

w = (bar_xy - bar_x * bar_y) / (bar_xx - bar_x * bar_x)
b = bar_y - w * bar_x
print("w = {0}".format(w))
print("b = {0}".format(b))
