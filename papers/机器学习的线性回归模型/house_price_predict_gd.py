import numpy as np

#X = np.array([2104, 1600, 2400, 1416, 3000])
#Y = np.array([3999.00, 3299.00, 3690.00, 2320.00, 5399.00])
X = np.array([0.434, 0.116, 0.621, 0.000, 1.000])
Y = np.array([0.545, 0.318, 0.445, 0.000, 1.000])

def cost(X, Y, a, b):
    s = 0
    for i in range(X.size):
        s += (Y[i] - (a*X[i] + b))**2
    return s * (1./2*Y.size)

def update_a(X, Y, a, b, eta):
    s = 0
    for i in range(X.size):
        s += ((a*X[i] + b)-Y[i])*X[i]
    return a - eta * s * (1./Y.size)

def update_b(X, Y, a, b, eta):
    s = 0
    for i in range(X.size):
        s += ((a*X[i] + b)-Y[i])
    return b - eta * s * (1./Y.size)

a = 0
b = 0
eta = 0.01

for i in range(10):
#for i in range(1000):
    a_new = update_a(X, Y, a, b, eta)
    b_new = update_b(X, Y, a, b, eta)
    cost_new = cost(X, Y, a_new, b_new)
    diff = abs(cost(X, Y, a, b) - cost(X, Y, a_new, b_new))
    print("a = {0}, b = {1}, cost = {2}, diff = {3}".format(a_new, b_new, cost_new, diff))
    a = a_new
    b = b_new
