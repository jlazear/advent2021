def parse_input(fname='input.txt'):
    with open(fname) as f:
        start1 = int(f.readline().strip().split(':')[1])
        start2 = int(f.readline().strip().split(':')[1])
    return start1, start2

def roll(max_val=100):
    i = 0
    while True:
        i += 1
        if i == max_val+1:
            i = 1
        yield i

def play(start1, start2, max_val=100, win_score=1000):
    pos1 = start1
    pos2 = start2

    dice = roll(max_val=max_val)
    score1 = 0
    score2 = 0
    turn = 1
    n_roll = 0
    while score1 < win_score and score2 < win_score:
        step = next(dice) + next(dice) + next(dice)
        n_roll += 3
        if turn == 1:
            pos1 += step
            while pos1 > 10:
                pos1 -= 10
            score1 += pos1
            turn = 2
        else:
            pos2 += step
            while pos2 > 10:
                pos2 -= 10
            score2 += pos2
            turn = 1
    return n_roll, pos1, pos2, score1, score2, turn
        
start1, start2 = parse_input()
n_roll, pos1, pos2, score1, score2, turn = play(start1, start2)

result = n_roll * (score1 if (turn == 1) else score2)
print(f"{result = }")