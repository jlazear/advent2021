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


def is_valid(arr, ij):
    imax, jmax = arr.shape
    imax -= 1
    jmax -= 1
    i, j = ij

    if i < 0 or i > imax or j < 0 or j > jmax:
        return False
    else:
        return True

def find_adjacent(arr, ij):
    i, j = ij
    adjacent = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
    adjacent = [ij for ij in adjacent if is_valid(arr, ij)]
    return adjacent


def size_basin_dfs(arr, ij_min):
    size = 1
    basin = set((ij_min,))
    i, j = ij_min
    candidates = find_adjacent(arr, ij_min)
    candidates = [(ij_min, candidate) for candidate in candidates if candidate not in basin]

    while candidates:
        candidate = candidates.pop()
        ij_ref, ij = candidate
        if (arr[ij] == 9) or (arr[ij_ref] >= arr[ij]):
            continue
        else:
            basin.add(ij)
            new_candidates = find_adjacent(arr, ij)
            new_candidates = [(ij_min, new_candidate) for new_candidate in new_candidates if new_candidate not in basin]
            candidates.extend(new_candidates)
    

    return len(basin)

basin_sizes = [size_basin_dfs(arr, ij) for ij in minima]
basin_sizes = sorted(basin_sizes)

print(np.product(basin_sizes[-3:]))
