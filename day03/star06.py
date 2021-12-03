with open('input.txt') as f:
    lines = [line.strip() for line in f.readlines()]
lines2 = lines.copy()

num_lines = len(lines)

i = 0
while len(lines) > 1:
    num_lines = len(lines)
    pos_sum = 0
    for line in lines:
        val = int(line[i])
        pos_sum += val
    bit_val = '1' if pos_sum >= num_lines - pos_sum else '0'
    lines = [line for line in lines if line[i] == bit_val]
    i += 1

oxygen_gen_rating = eval('0b' + lines[0])

lines = lines2
i = 0
while len(lines) > 1:
    num_lines = len(lines)
    pos_sum = 0
    for line in lines:
        val = int(line[i])
        pos_sum += val
    bit_val = '1' if pos_sum < num_lines - pos_sum else '0'
    lines = [line for line in lines if line[i] == bit_val]
    i += 1

co2_scrubber_rating = eval('0b' + lines[0])

print(oxygen_gen_rating, co2_scrubber_rating)
print(oxygen_gen_rating*co2_scrubber_rating)