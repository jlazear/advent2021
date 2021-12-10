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
    return stack

scores_dict = {'(': 1,
               '[': 2,
               '{': 3,
               '<': 4}

def score_stack(stack, scores_dict):
    score = 0
    while stack:
        next = stack.pop()
        score = score*5 + scores_dict[next]
    return score

scores = []
with open('input.txt') as f:
    for line in f:
        line = line.strip()
        stack = evaluate_line(line)
        if type(stack) is list:
            scores.append(score_stack(stack, scores_dict))

scores = sorted(scores)

print(scores[len(scores)//2])