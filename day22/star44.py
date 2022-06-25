def parse_input(fname='input.txt'):
    commands = []
    with open(fname) as f:
        for line in f:
            cmd, range_str = line.strip().split()
            cmd = 1 if cmd == 'on' else 0
            xyz = parse_range(range_str)
            commands.append((cmd, xyz))
    return commands

def parse_range(s):
    slist = s.split(',')
    slist = [dimstr.split('=')[1] for dimstr in slist]
    slist = tuple(tuple(map(int, x.split('..'))) for x in slist)
    return slist

def intersection(xyz1, xyz2):
    if xyz2 is None:
        return None
    ((x1min, x1max), (y1min, y1max), (z1min, z1max)) = xyz1
    ((x2min, x2max), (y2min, y2max), (z2min, z2max)) = xyz2    

    x3min = max(x1min, x2min)
    y3min = max(y1min, y2min)
    z3min = max(z1min, z2min)

    x3max = min(x1max, x2max)
    y3max = min(y1max, y2max)
    z3max = min(z1max, z2max)

    if (x3min <= x3max) and (y3min <= y3max) and (z3min <= z3max):
        return ((x3min, x3max), (y3min, y3max), (z3min, z3max))
    return False

def add_cube(cmd, xyz, on_list, off_list, xyz_lim=None):
    if (xyz_lim is not None) and not intersection(xyz, xyz_lim):
        return on_list, off_list
    if cmd:  # ON
        on_len = len(on_list)
        off_len = len(off_list)

        on_list.append(xyz)

        for i in range(on_len):
            xyz2 = on_list[i]
            xyz_int = intersection(xyz, xyz2)
            if xyz_int:
                off_list.append(xyz_int)
        
        for j in range(off_len):
            xyz2 = off_list[j]
            xyz_int = intersection(xyz, xyz2)
            if xyz_int:
                on_list.append(xyz_int)
    else:  # OFF
        off_len = len(off_list)
        for xyz2 in on_list:
            xyz_int = intersection(xyz, xyz2)
            if xyz_int:
                off_list.append(xyz_int)
        
        for xyz2 in off_list[:off_len]:
            xyz_int = intersection(xyz, xyz2)
            if xyz_int:
                on_list.append(xyz_int)

    return on_list, off_list

def volume(xyzs):
    try:
        xyzs[0][0][0]
        return sum([volume(xyz) for xyz in xyzs])
    except TypeError:
        ((xmin, xmax), (ymin, ymax), (zmin, zmax)) = xyzs
        return (xmax - xmin + 1)*(ymax - ymin + 1)*(zmax - zmin + 1)


commands = parse_input('input.txt')

xyz_lim = None # ((-50, 50), (-50, 50), (-50, 50))
on_list = []
off_list = []
for cmd, xyz in commands:
    print(f"{cmd = }, {xyz = }")
    on_list, off_list = add_cube(cmd, xyz, on_list, off_list, xyz_lim=xyz_lim)

pos_volume = volume(on_list)
neg_volume = volume(off_list)
tot_volume = pos_volume - neg_volume
print(f"{pos_volume = }, {neg_volume = }")
print(f"number of cubes on = {tot_volume = }")