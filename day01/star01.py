import numpy as np

data = np.loadtxt('input.txt')
ddata = np.diff(data)
print(np.sum(ddata > 0))
