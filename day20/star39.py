from collections import defaultdict

def parse_input(fname='input.txt'):
    rules = []
    with open(fname) as f:
        rulestr = f.readline()
        for c in rulestr.strip():
            rules.append(1 if c == '#' else 0)
        _ = f.readline()

        img = defaultdict(int)
        i = 0
        for line in f:
            j = 0
            for c in line.strip():
                if c == '#':
                    img[(i, j)] = 1
                j += 1
            i += 1
    return rules, img

def filter(i, j, img, rules):
    index = 0
    index += img[(i-1, j-1)] << 8
    index += img[(i-1, j+0)] << 7
    index += img[(i-1, j+1)] << 6
    index += img[(i+0, j-1)] << 5
    index += img[(i+0, j+0)] << 4
    index += img[(i+0, j+1)] << 3
    index += img[(i+1, j-1)] << 2
    index += img[(i+1, j+0)] << 1
    index += img[(i+1, j+1)] << 0
    # print(f"{index = }, {rules[index] = }")  #DELME
    return rules[index]

def iterate(img, rules):
    iis = [v[0] for v in img]
    jjs = [v[1] for v in img]
    min_i, max_i = min(iis), max(iis)
    min_j, max_j = min(jjs), max(jjs)

    default_val = rules[511] if img.default_factory() else rules[0]
    new_img = defaultdict(lambda: default_val)
    for i in range(min_i, max_i+1):
        for j in range(min_j, max_j+1):
            new_img[i, j] = filter(i, j, img, rules)

    return new_img

def make_img(img, pad=3):
    iis = [v[0] for v in img]
    jjs = [v[1] for v in img]
    min_i, max_i = min(iis) - pad, max(iis) + pad
    min_j, max_j = min(jjs) - pad, max(jjs) + pad


    img_s = []
    for i in range(min_i, max_i+1):
        row = []
        for j in range(min_j, max_j+1):
            row.append('#' if img[i, j] else '.')
        img_s.append(''.join(row))
    return '\n'.join(img_s)



rules, img = parse_input('input.txt')
print(make_img(img))
img = iterate(img, rules)
print(make_img(img))
img = iterate(img, rules)
print(make_img(img))

print(f"{sum(img.values())}")