import numpy as np

X = np.matrix([
    [1, 1, 1, 1, 1], 
    [1985, 1534, 1427, 1380, 1494], 
    [4, 3, 3, 3, 3]]).T
Y = np.matrix([299.900, 314.900, 198.999, 212.000, 242.500]).T

a = (X.T * X).I * X.T * Y
print("a = {0}".format(a))
