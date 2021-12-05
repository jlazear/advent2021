from collections import defaultdict

def parse_file(fname):
    pairs = []
    for line in open(fname):
        start_str, end_str = line.strip().split('->')
        start_x, start_y = map(int, start_str.split(','))
        end_x, end_y = map(int, end_str.split(','))
        pairs.append((start_x, start_y, end_x, end_y))
    return pairs

def is_hor_or_vert(pair):
    sx, sy, ex, ey = pair
    if (sx == ex):
        return 1
    elif (sy == ey):
        return 2
    else:
        return 0

d = defaultdict(int)

pairs = parse_file('input.txt')
for pair in pairs:
    hor_or_vert = is_hor_or_vert(pair)
    if hor_or_vert == 1:
        x, sy, _, ey = pair
        sy, ey = min(sy, ey), max(sy, ey)
        for y in range(sy, ey+1):
            d[(x, y)] += 1
    elif hor_or_vert == 2:
        sx, y, ex, _ = pair
        sx, ex = min(sx, ex), max(sx, ex)
        for x in range(sx, ex+1):
            d[(x, y)] += 1
    else:
        sx, sy, ex, ey = pair
        dx = 1 if ex > sx else -1
        dy = 1 if ey > sy else -1
        for i in range(abs(ex - sx) + 1):
            d[(sx + dx*i, sy + dy*i)] += 1

num = 0
for key, value in d.items():
    if value >= 2:
        num += 1

print(num)