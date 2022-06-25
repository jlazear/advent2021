import numpy as np

drefs = []

with open('output.txt') as f:
    for line in f:
        if line.startswith('dref'):
            dref = eval(line.split('=')[1])
            dref = np.array(dref, dtype='int')
            drefs.append(dref)

drefs = np.array(drefs, dtype='int')

max_mag = 0
for dref1 in drefs:
    for dref2 in drefs:
       mag = np.sum(np.abs(dref2 - dref1)) 
       max_mag = max(mag, max_mag)

print(f"{max_mag = }")