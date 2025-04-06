import numpy as np

np.set_printoptions(precision=3)

X = np.array([2104.0, 1600.0, 2400.0, 1416.0, 3000.0])
Y = np.array([399.900, 329.900, 369.000, 232.000, 539.900])

def min_max_normalization(x, Max, Min):
    return (x - Min) / (Max - Min)

print(X)
print(Y)

Max = max(X)
Min = min(X)
for i in range(X.size):
    X[i] = min_max_normalization(X[i], Max, Min)

Max = max(Y)
Min = min(Y)
for i in range(Y.size):
    Y[i] = min_max_normalization(Y[i], Max, Min)

print(X)
print(Y)
