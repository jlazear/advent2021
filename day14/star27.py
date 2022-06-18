from collections import Counter, deque

def parse_input(fname='input.txt'):
    rules = {}
    with open(fname) as f:
        template = deque(f.readline().strip())
        f.readline()

        for line in f:
            left, right = line.strip().split(' -> ')
            rules[left] = right
    
    return template, rules

def update(polymer, rules, counter):
    new_polymer = deque()
    while polymer:
        left = polymer.popleft()
        new_polymer.append(left)
        if polymer:
            right = polymer[0]
            toadd = rules[left + right]
            new_polymer.append(toadd)
            counter[toadd] += 1
    return new_polymer, counter
        

template, rules = parse_input('input.txt')
counter = Counter(template)

polymer = template
N = 10
for i in range(1, N+1):
    polymer, counter = update(polymer, rules, counter)
    mc = counter.most_common()
    delta = mc[0][1] - mc[-1][1]
    print("{}: len {}, delta {}".format(i, len(polymer), delta))