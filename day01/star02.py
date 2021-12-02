import numpy as np

data = np.loadtxt('input.txt')
ddata = data[:-2] + data[1:-1] + data[2:]
ddata2 = np.diff(ddata)

print(np.sum(ddata2 > 0))

