import numpy as np
from numpy.linalg import norm

with open('input.txt') as f:
    crabs = np.array(list(map(int, f.readline().split(','))), dtype='int')

minima = []
for pos in range(crabs.min(), crabs.max()+1):
    delta = np.abs(crabs - pos)
    cost = delta*(delta+1)/2
    fuel = np.sum(cost)
    minima.append(fuel)

print(int(np.min(minima)))