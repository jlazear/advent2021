aim = 0
horizontal = 0
depth = 0

with open('input.txt') as f:
	for line in f:
		cmd, arg = line.split()
		arg = int(arg)

		if cmd == 'forward':
			horizontal += arg
			depth += aim*arg
		elif cmd == 'down':
			aim += arg
		elif cmd == 'up':
			aim -= arg
		else:
			print("FAILURE")

print("horizontal = ", horizontal)
print("depth = ", depth)
print("product = ", horizontal*depth)
