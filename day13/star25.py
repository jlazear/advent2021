def parse_input(fname='input.txt'):
    dot_coords = []
    folds = []
    with open(fname) as f:
        line = f.readline()
        while line != '\n':
            x, y = line.strip().split(',')
            x, y = int(x), int(y)
            dot_coords.append((x, y))
            line = f.readline()

        for line in f:
            line = line.strip()
            _, _, s = line.split()
            direction, value = s.split('=')
            folds.append((direction, int(value)))
    return set(dot_coords), folds

def fold(direction, value, dot_coords):
    new_coords = []
    for x, y in dot_coords:
        if direction == 'x':
            if x > value:
                x = 2*value - x
        elif direction == 'y':
            if y > value:
                y = 2*value - y
        else:
            raise("invalid direction {}".format(direction))
        new_coords.append((x, y))
    return set(new_coords)

        

dot_coords, folds = parse_input()

coords2 = fold(*folds[0], dot_coords)

