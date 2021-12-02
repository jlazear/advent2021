horizontal = 0
depth = 0

with open('input.txt') as f:
	for line in f:
		cmd, arg = line.split()
		arg = int(arg)

		if cmd == 'forward':
			horizontal += arg
		elif cmd == 'down':
			depth += arg
		elif cmd == 'up':
			depth -= arg
		else:
			print("FAILURE")

print("horizontal = ", horizontal)
print("depth = ", depth)
print("product = ", horizontal*depth)
