import numpy as np

with open('input.txt') as f:
    arr = []
    for line in f:
        arr.append([int(x) for x in line.strip()])

arr = np.array(arr, dtype='int')


def check_min(arr, i, j):
    imax, jmax = arr.shape
    imax -= 1
    jmax -= 1

    if i == 0:  # top row
        if j == 0:  # top left
            if (arr[i, j] < arr[i+1, j]) and (arr[i, j] < arr[i, j+1]):
                return True
        elif j == jmax:  # top right
            if (arr[i, j] < arr[i+1, j]) and (arr[i, j] < arr[i, j-1]):
                return True
        else:  # top row, not corners
            if (arr[i, j] < arr[i+1, j]) and (arr[i, j] < arr[i, j-1]) and (arr[i, j] < arr[i, j+1]):
                return True
    elif i == imax:  # bottom row
        if j == 0:  # bottom left
            if (arr[i, j] < arr[i-1, j]) and (arr[i, j] < arr[i, j+1]):
                return True
        elif j == jmax:  # bottom right
            if (arr[i, j] < arr[i-1, j]) and (arr[i, j] < arr[i, j-1]):
                return True
        else:  # bottom row, not corners
            if (arr[i, j] < arr[i-1, j]) and (arr[i, j] < arr[i, j-1]) and (arr[i, j] < arr[i, j+1]):
                return True
    else:  # middle rows
        if j == 0:  # left column, not corners
            if (arr[i, j] < arr[i-1, j]) and (arr[i, j] < arr[i, j+1]) and (arr[i, j] < arr[i+1, j]):
                return True
        elif j == jmax:  # right column, not corners
            if (arr[i, j] < arr[i-1, j]) and (arr[i, j] < arr[i, j-1]) and (arr[i, j] < arr[i+1, j]):
                return True
        else:  # all middle
            if (arr[i, j] < arr[i-1, j]) and (arr[i, j] < arr[i, j-1]) and (arr[i, j] < arr[i+1, j]) and (arr[i, j] < arr[i, j+1]):
                return True
    return False

minima = []
for i in range(len(arr)):
    for j in range(len(arr[0])):
        if check_min(arr, i, j):
            minima.append((i, j))

risk = 0
for ij in minima:
    risk += arr[ij] + 1

print(risk)