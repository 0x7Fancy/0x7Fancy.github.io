import numpy as np
import matplotlib.pyplot as plt

X = np.array([35, 27, 10, 15, 21, 8])
Y = np.array([1, 1, 0, 0, 1, 0])

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def cost(X, Y, w, b):
    s = 0
    for i in range(X.size):
        s += (Y[i] * np.log(sigmoid(X[i]*w+b))) + ((1-Y[i]) * np.log(1-sigmoid(X[i]*w+b)))
    return s * (-1 / X.size)

def update_w(X, Y, w, b, eta):
    s = 0
    for i in range(X.size):
        s += (Y[i] - sigmoid(X[i]*w+b)) * X[i]
    return w - eta * s * (-1./Y.size)

def update_b(X, Y, w, b, eta):
    s = 0
    for i in range(X.size):
        s += (Y[i] - sigmoid(X[i]*w+b))
    return b - eta * s * (-1./Y.size)

w = 0
b = 0
eta = 0.001

#for i in range(10):
for i in range(100000):
    w = update_w(X, Y, w, b, eta)
    b = update_b(X, Y, w, b, eta)
    #print("{0}. w = {1}, b = {2}, cost = {3}".format(i, w, b, cost(X, Y, w, b)))
# end for

print("w = {0}, b = {1}, cost = {2}".format(w, b, cost(X, Y, w, b)))

x = np.linspace(0, 50, 10)
y = 1.0 / (1 + np.exp(-(w*x+b)))

plt.plot(X, Y, 'k.')
plt.plot(x, y, 'g-')

#y = w*x+b
#plt.plot(x, y)

plt.show()
