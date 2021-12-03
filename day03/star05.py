with open('input.txt') as f:
    lines = f.readlines()

num_lines = len(lines)

bit_sum = [0]*(len(lines[0]) - 1)
for line in lines:
    line = line.strip()
    for i, x in enumerate(line):
        # print(x)
        # print(int(x))
        bit_sum[i] += int(x)

print(bit_sum)

gamma_arr = ['0' if x < 500 else '1' for x in bit_sum]
epsilon_arr = ['0' if x > 500 else '1' for x in bit_sum]

print(gamma_arr)

gamma = eval('0b' + ''.join(gamma_arr))
epsilon = eval('0b' + ''.join(epsilon_arr))

print(gamma, epsilon)
print(gamma*epsilon)
