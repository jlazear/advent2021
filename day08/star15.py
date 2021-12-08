from collections import defaultdict

seg_to_numbers = {'a': set([0, 2, 3, 5, 6, 7, 8, 9]),
                  'b': set([0, 5, 6, 8, 9]),
                  'c': set([0, 1, 2, 3, 4, 7, 8, 9]),
                  'd': set([2, 3, 4, 5, 6, 8, 9]),
                  'e': set([0, 2, 6, 8]),
                  'f': set([0, 1, 3, 4, 5, 6, 7, 8, 9]),
                  'g': set([0, 2, 3, 5, 6, 8, 9])}

nseg_to_numbers = {0: set(),
                   1: set(),
                   2: set([1]),
                   3: set([7]),
                   4: set([4]),
                   5: set([2, 3, 5]),
                   6: set([0, 6, 9]),
                   7: set([8])}

def parse_line(line):
    first, second = line.strip().split('|')
    codes = [''.join(sorted(x)) for x in first.split()]
    signals = [''.join(sorted(x)) for x in second.split()]

    code_to_num_dict = defaultdict(lambda: set(range(10)))
    for code in codes:
        code_to_num_dict[code] &= nseg_to_numbers[len(code)]
    return code_to_num_dict, signals

def invert_code_to_num_dict(code_to_num_dict):
    num_to_seg_dict = defaultdict(lambda: set())
    for code, numset in code_to_num_dict.items():
        for num in numset:
            num_to_seg_dict[num] |= set([code])
    return num_to_seg_dict

def map_digits(code_to_num_dict):
    num_to_code_dict = invert_code_to_num_dict(code_to_num_dict)

    code_to_num_dict

    code7 = num_to_code_dict[7].pop()
    code1 = num_to_code_dict[1].pop()
    code4 = num_to_code_dict[4].pop()

    for code, numbers in code_to_num_dict.items():
        if 2 in numbers:
            if len(set(code) & set(code7)) == 3:
                code_to_num_dict[code] = set([3])
                break

    for code, numbers in code_to_num_dict.items():
        if 3 in numbers and len(numbers) > 1:
            code_to_num_dict[code] = set([2, 5])


    for code, numbers in code_to_num_dict.items():
        if 0 in numbers:
            if len(set(code) & set(code1)) == 1:
                code_to_num_dict[code] = set([6])
                break

    for code, numbers in code_to_num_dict.items():
        if 6 in numbers and len(numbers) > 1:
            code_to_num_dict[code] = set([0, 9])



    for code, numbers in code_to_num_dict.items():
        if 0 in numbers:
            if len(set(code) & set(code4)) == 3:
                code_to_num_dict[code] = set([0])
            elif len(set(code) & set(code4)) == 4:
                code_to_num_dict[code] = set([9])

    for code, numbers in code_to_num_dict.items():
        if 2 in numbers:
            if len(set(code) & set(code4)) == 2:
                code_to_num_dict[code] = set([2])
            elif len(set(code) & set(code4)) == 3:
                code_to_num_dict[code] = set([5])


    c2nd = {key: value.pop() for key, value in code_to_num_dict.items()}

    return c2nd


with open('input.txt') as f:
    values = []
    for line in f:
        code_to_num_dict, signals = parse_line(line)
        digits_map = map_digits(code_to_num_dict)
        values.append([digits_map[signal] for signal in signals])
    

num1478 = 0
for row in values:
    for x in row:
        if x in [1, 4, 7, 8]:
           num1478 += 1

print(num1478) 