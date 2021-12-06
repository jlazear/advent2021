import numpy as np
from collections import defaultdict

with open('input.txt') as f:
    fish = list(map(int, f.readline().split(',')))

day = 0
day_max = 256

ages, numbers = np.unique(fish, return_counts=True)
d = defaultdict(int)
for i, age in enumerate(ages):
    d[age] = numbers[i]

print(d)

while day < day_max:
    print("day = ", day)
    d2 = defaultdict(int)
    for key, value in d.items():
        if key == 0:
            d2[8] = value
            d2[6] += value
        else:
            d2[key-1] += value
    d = d2
    day += 1

s = 0
for value in d.values():
    s += value

print(s)