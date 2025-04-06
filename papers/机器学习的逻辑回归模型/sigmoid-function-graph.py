import numpy as np
import matplotlib.pyplot as plt

plt.xlim(-10, 10)
plt.ylim(0, 1)

x = np.linspace(-10,10,100)
y = 1/(1+np.exp(-x))
plt.plot(x,y,'r-')
plt.xlabel('x')
plt.ylabel('y')
plt.title(r'$y=\frac{1}{1+e^{-x}}$')

plt.show()
