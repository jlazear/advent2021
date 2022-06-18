from collections import Counter

def parse_input(fname='input.txt'):
    rules = {}
    with open(fname) as f:
        template = f.readline().strip()
        f.readline()

        for line in f:
            left, right = line.strip().split(' -> ')
            rules[left] = right
    
    pairs = [template[i:i+2] for i in range(len(template)-1)]
    pair_counter = Counter(pairs)
    counter = Counter(template)
    return pair_counter, rules, counter

def update(pair_counter, rules, counter):
    new_pair_counter = Counter()
    for pair in pair_counter:
        new_element = rules[pair]
        new_pair1 = pair[0] + new_element
        new_pair2 = new_element + pair[1]
        n_elem = pair_counter[pair]

        new_pair_counter[new_pair1] += n_elem
        new_pair_counter[new_pair2] += n_elem
        counter[new_element] += n_elem
    return new_pair_counter, counter
        
print("=== FOR test.txt ===")
pair_counter, rules, counter = parse_input('test.txt')

N = 40
for i in range(1, N+1):
    pair_counter, counter = update(pair_counter, rules, counter)
    mc = counter.most_common()
    delta = mc[0][1] - mc[-1][1]
    print("{}: len {}, delta {}".format(i, sum(counter.values()), delta))


print("=== FOR input.txt ===")
pair_counter, rules, counter = parse_input('input.txt')

N = 40
for i in range(1, N+1):
    pair_counter, counter = update(pair_counter, rules, counter)
    mc = counter.most_common()
    delta = mc[0][1] - mc[-1][1]
    print("{}: len {}, delta {}".format(i, sum(counter.values()), delta))