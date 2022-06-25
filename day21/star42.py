from collections import defaultdict

def parse_input(fname='input.txt'):
    with open(fname) as f:
        start1 = int(f.readline().strip().split(':')[1])
        start2 = int(f.readline().strip().split(':')[1])
    return start1, start2

def play(start1=10, start2=7, win_score=21):
    step_dict = {3: 1,
                4: 3,
                5: 6,
                6: 7,
                7: 6,
                8: 3,
                9: 1}

    valids = {(start1, start2, 0, 0, 1): 1}
    done = defaultdict(int)
    i = 0
    while valids:
        print(f"{i = }")  #DELME
        i += 1  #DELME
        new_valids = defaultdict(int) 
        for (pos1, pos2, score1, score2, turn), n_old in valids.items():
            if turn == 1:  # odd turns belong to player 1
                for step, n_new in step_dict.items():
                    newpos1 = pos1 + step
                    while newpos1 > 10:
                        newpos1 -= 10
                    new_score1 = score1 + newpos1
                    if new_score1 >= win_score:
                        done[(newpos1, pos2, new_score1, score2, turn)] += n_old*n_new
                    else:
                        new_valids[(newpos1, pos2, new_score1, score2, 2)] += n_old*n_new
            elif turn == 2:  # even turns belong to player 2
                for step, n_new in step_dict.items():
                    newpos2 = pos2 + step
                    while newpos2 > 10:
                        newpos2 -= 10
                    new_score2 = score2 + newpos2
                    if new_score2 >= win_score:
                        done[(pos1, newpos2, score1, new_score2, turn)] += n_old*n_new
                    else:
                        new_valids[(pos1, newpos2, score1, new_score2, 1)] += n_old*n_new
        valids = new_valids
    return done
                    
def calculate_scores(done):
    score1 = 0
    score2 = 0
    for (_, _, _, _, winner), n in done.items():
        if winner == 1:
            score1 += n
        else:
            score2 += n
    return score1, score2

start1, start2 = parse_input('input.txt')
done = play(start1, start2)
score1, score2 = calculate_scores(done)

print(f"{score1 = }, {score2 = }")
print(f"{max(score1, score2) = }")
