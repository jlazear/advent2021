import numpy as np
from scipy.signal import convolve2d

def read_input(fname):
    with open(fname) as f:
        arr = [list(map(int, line.strip())) for line in f.readlines()]
    return np.array(arr, dtype='int')

def step(arr):
    arr += 1

    num_flashes = 0
    flash_arr = arr > 9
    num_flashes += np.sum(flash_arr)
    zero_arr = np.ones_like(arr)
    zero_arr[flash_arr] = 0
    arr[flash_arr] = 0
    iteration_flag = flash_arr.any()
    kernel = np.array([[1, 1, 1],
                       [1, 0, 1],
                       [1, 1, 1]])
    
    while iteration_flag:
        arr += convolve2d(flash_arr, kernel, mode='same')
        flash_arr = arr > 9
        num_flashes += np.sum(flash_arr)
        zero_arr[flash_arr] = 0
        arr[flash_arr] = 0
        iteration_flag = flash_arr.any()
    
    arr = arr*zero_arr
    return arr, num_flashes

n_steps = 100

def print_arr(arr):
    print('\n'.join([''.join(map(str, row)) for row in arr]))

arr = read_input('input.txt')
# print("Before any steps:")
# print_arr(arr)

num_flashes = 0
n_step = 0
while num_flashes != np.product(np.shape(arr)):
    n_step += 1
    # print("\nAfter step {0}".format(i+1))
    arr, num_flashes = step(arr)
    # print_arr(arr)

print("sync step = ", n_step)