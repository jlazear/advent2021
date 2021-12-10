def evaluate_line(line):
    match_dict = {')': '(',
             ']': '[',
             '}': '{',
             '>': '<'}
    stack = []

    for c in line:
        if c in '([{<':
            stack.append(c)
        elif c in ')]}>':
            if match_dict[c] != stack.pop():
                return c
        else:
            raise('Invalid character')
    return True

scores_dict = {')': 3,
               ']': 57,
               '}': 1197,
               '>': 25137}

fails = []
with open('input.txt') as f:
    for line in f:
        line = line.strip()
        fail = evaluate_line(line)
        if fail is not True:
            print("fail = ", fail)  #DELME
            fails.append(fail)

score = 0
for fail in fails:
    score += scores_dict[fail]

print(score)