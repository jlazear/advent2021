import numpy as np

def y(n, vy):
    return n*vy - n*(n+1)/2

ymin = -122
ymax = -74

vy_max = 150
valid_vy = np.array([False]*vy_max, dtype='bool')
max_y = np.array([0]*vy_max, dtype='int')
n_valids = [-1]*vy_max
for vy in range(vy_max):
    n = 1
    yn = y(n, vy)
    max_y[vy] = yn
    while yn >= ymin:
        if yn > max_y[vy]:
            max_y[vy] = yn
        if yn <= ymax:
            valid_vy[vy] = True
            n_valids[vy] = n
            break
        n += 1
        yn = y(n, vy)

print(f"ymax = {np.max(max_y[valid_vy])}")