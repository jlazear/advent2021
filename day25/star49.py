import numpy as np

def parse_input(fname='input.txt'):
    cdict = {'.': 0, '>': 1, 'v': 2}
    with open(fname) as f:
        rows = [[cdict[c] for c in line.strip()] for line in f]
    return np.array(rows, dtype='int')

def iterate(data):
    # advance the >'s
    data2 = np.zeros_like(data)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if data[i][j] == 1:
                jnext = j+1 if j < data.shape[1] - 1 else 0
                if data[i][jnext] == 0:
                    data2[i][jnext] = 1
                else:
                    data2[i][j] = 1
            elif data[i][j] == 2:
                data2[i][j] = 2
    
    # advance the v's
    data3 = np.zeros_like(data) 
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if data2[i][j] == 2:
                inext = i+1 if i < data.shape[0] - 1 else 0
                if data2[inext][j] == 0:
                    data3[inext][j] = 2
                else:
                    data3[i][j] = 2
            elif data2[i][j] == 1:
                data3[i][j] = 1

    stopped = (data3 == data).all()
    return data3, stopped

def print_data(data):
    cdict = {0: '.', 1: '>', 2: 'v'}
    return '\n'.join([''.join([cdict[c] for c in row]) for row in data])


data = parse_input('input.txt')
# print(print_data(data))
i = 0
while True:
    data, stopped = iterate(data)
    i += 1
    if stopped:
        print(f"STOPPED after {i} steps")
        break
    # print(f"After {i} steps:")
    # print(print_data(data) + '\n')


