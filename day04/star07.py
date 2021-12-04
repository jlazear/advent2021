import numpy as np

def check_rows(arr, drawn):
    for row in arr:
        win = True
        for val in row:
            win = val in drawn
            if not win:
                break
        if win:
            return True
    return False

def check_cols(arr, drawn):
    return check_rows(arr.T, drawn)

def check_diags(arr, drawn):
    diag1 = arr.diagonal()
    diag2 = np.fliplr(arr).diagonal()
    arr2 = np.array([diag1, diag2])
    return check_rows(arr2, drawn)

def check_board(arr, drawn):
    return (check_rows(arr, drawn) or check_cols(arr, drawn) or check_diags(arr, drawn))

def read_board(f):
    vals = []
    for _ in range(5):
        line = [int(x) for x in f.readline().split()]
        vals.append(line)
    return np.array(vals)

with open('input.txt') as f:
    numbers = [int(i) for i in f.readline().split(',')]

    boards = []
    while f.readline():
        boards.append(read_board(f))

print(numbers)

done = False
save_board = False
i = 5
while not done:
    drawn = numbers[:i]
    for board in boards:
        if check_board(board, drawn):
            done = True
            save_board = board
            break
    if save_board is not False:
        break
    i += 1

print(drawn)
print(board)

print(np.sum(save_board*(~np.isin(save_board, drawn))) * drawn[-1])