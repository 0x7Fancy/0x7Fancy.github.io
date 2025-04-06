import numpy as np

X0 = np.ones((5, 1))
X1 = np.array([0.434, 0.116, 0.621, 0.000, 1.000]).reshape(-1, 1)
X = np.hstack((X0, X1))
y = np.array([0.545, 0.318, 0.445, 0.000, 1.000]).reshape(-1, 1)

def gradient_descent(X, y, eta, theta, max_iter):
    for i in range(max_iter):
        diff = np.dot(X, theta) - y
        cost = (1./2*y.size) * np.sum(diff ** 2)

        gradient = (1./y.size) * np.dot(np.transpose(X), diff)
        theta = theta - eta * gradient

        print("theta: {0} {1}, cost: {2}".format(theta[0,0], theta[1,0], cost))
    return theta

theta_init = np.array([0, 0]).reshape(-1, 1)
eta = 0.01
max_iter = 1000

gradient_descent(X, y, eta, theta_init, max_iter)
