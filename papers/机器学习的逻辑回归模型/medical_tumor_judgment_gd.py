import numpy as np
import matplotlib.pyplot as plt

X = np.array([35, 27, 10, 15, 21, 8])
Y = np.array([1, 1, 0, 0, 1, 0])

def fx(x, w, b):
    return np.exp(w*x+b) / (1 + np.exp(w*x+b))

def update_w(X, Y, w, b, eta):
    s = 0
    for i in range(X.size):
        s += (fx(X[i], w, b) - Y[i])*X[i]
    return w - eta * s * (1./Y.size)

def update_b(X, Y, w, b, eta):
    s = 0
    for i in range(X.size):
        s += (fx(X[i], w, b) - Y[i])
    return b - eta * s * (1./Y.size)

def cost(X, Y, w, b):
    s = 0
    for i in range(X.size):
        s += np.log(1 + np.exp(w*X[i]+b)) - Y[i]*(w*X[i]+b)
    return s * (1 / X.size)

w = 0
b = 0
eta = 0.001

#for i in range(10):
for i in range(100000):
    w = update_w(X, Y, w, b, eta)
    b = update_b(X, Y, w, b, eta)
    print("{0}. w = {1}, b = {2}, cost = {3}".format(i, w, b, cost(X, Y, w, b)))
    
print("w = {0}, b = {1}, cost = {2}".format(w, b, cost(X, Y, w, b)))


x = np.linspace(0, 50, 10)
y = 1.0 / (1 + np.exp(-(w*x+b)))

plt.plot(X, Y, 'k.')
plt.plot(x, y, 'g-')

#y = w*x+b
#plt.plot(x, y)

plt.show()
