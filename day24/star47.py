fname = 'input.txt'
with open(fname) as f:
    blocks = f.read().split('inp w\n')[1:]

blocks = [block.split('\n') for block in blocks]

coefficients = []
a = []
b = []
c = []
for block in blocks:
    c0 = int(block[3].split()[-1])
    c1 = int(block[4].split()[-1])
    c2 = int(block[14].split()[-1])
    coefficients.append((c0, c1, c2))
    a.append(c0)
    b.append(c1)
    c.append(c2)

for x in list(zip(range(len(coefficients)), coefficients)):
    print(x)



equations = (
f"""
w13 = w0 + {c[0] + b[13]}
w12 = w1 + {c[1] + b[12]}
w11 = w10 + {c[10] + b[11]}
w9 = w6 + {c[6] + b[9]}
w8 = w7 + {c[7] + b[8]}
w5 = w2 + {c[2] + b[5]}
w4 = w3 + {c[3] + b[4]}
""")


print("\n\neach of the 14 inp blocks have the same structure, with 3 coefficients a_i, b_i, c_i")
print("if a_i = 1, then push a base-26 digit (d = w_i + c_i) onto the LS digit of z")
print("if a_i = 26, then pop the LS base-26 digit into x, and if w_i != d + b_i then push a digit (d = w_i + c_i) onto the LS digit of z")
print("since there are 7 pushes and 7 pops, need all of the pop conditions to be true so don't have extra digits")
print("this gives us the equations...")
print(equations)
print("which imply")
print("w_max = 99999795919456 (manually calculated, so may not match equations)")
print("w_min = 45311191516111 (manually calculated, so may not match equations)")