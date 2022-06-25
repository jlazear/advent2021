import numpy as np

def parse_input(fname='input.txt'):
    scanners = {}

    scanner_number = None
    with open(fname) as f:
        for line in f:
            if line.startswith('\n'):
                pass
            elif line.startswith('---'):
                scanner_number = int(line.split()[2])
                scanners[scanner_number] = []
            else:
                coords = line.strip().split(',')
                coords = tuple(map(int, coords))
                scanners[scanner_number].append(coords)
    
    return scanners

# def delta_scanners(scanners, ref=None):
#     dscanners = {}
#     for key, coords in scanners.items():
#         if ref is None:
#             ref = min(coords)
#         new_coords = []
#         for coord in coords:
#             new_coord = (coord[0] - ref[0], coord[1] - ref[1], coord[2] - ref[2])
#             new_coords.append(new_coord)
#         dscanners[key] = new_coords
    
#     return dscanners

def orient(coords, orientation=0):
    orientation_dict = {
        0: lambda x, y, z: (x, y, z),
        1: lambda x, y, z: (x, -y, -z),
        2: lambda x, y, z: (-x, -y, z),
        3: lambda x, y, z: (-x, y, -z),
        4: lambda x, y, z: (x, z, -y),
        5: lambda x, y, z: (x, -z, y),
        6: lambda x, y, z: (-x, z, y),
        7: lambda x, y, z: (-x, -z, -y),
        8: lambda x, y, z: (z, x, y),
        9: lambda x, y, z: (z, -x, -y),
        10: lambda x, y, z: (-z, -x, y),
        11: lambda x, y, z: (-z, x, -y),
        12: lambda x, y, z: (-z, y, x),
        13: lambda x, y, z: (z, -y, x),
        14: lambda x, y, z: (z, y, -x),
        15: lambda x, y, z: (-z, -y, -x),
        16: lambda x, y, z: (y, z, x),
        17: lambda x, y, z: (y, -z, -x),
        18: lambda x, y, z: (-y, z, -x),
        19: lambda x, y, z: (-y, -z, x),
        20: lambda x, y, z: (-y, x, z),
        21: lambda x, y, z: (y, -x, z),
        22: lambda x, y, z: (y, x, -z),
        23: lambda x, y, z: (-y, -x, -z),
    }

    try:
        new_coords = [orientation_dict[orientation](*coord) for coord in coords]
    except TypeError:
        new_coords = orientation_dict[orientation](*coords)
    return new_coords

def offset(coords, ref=None):
    if ref is None:
        ref = min(coords)
    new_coords = set([(coord[0] - ref[0], coord[1] - ref[1], coord[2] - ref[2]) for coord in coords])
    return new_coords


def deorient(coords, orientation=0):
    deorientation_dict = {
        0: lambda x, y, z: (x, y, z),
        1: lambda x, y, z: (x, -y, -z), # (x, -y, -z),
        2: lambda x, y, z: (-x, -y, z), # (-x, -y, z),
        3: lambda x, y, z: (-x, y, -z), # (-x, y, -z),
        4: lambda x, y, z: (x, -z, y), # (x, z, -y),
        5: lambda x, y, z: (x, z, -y), # (x, -z, y),
        6: lambda x, y, z: (-x, z, y), # (-x, z, y),
        7: lambda x, y, z: (-x, -z, -y), # (-x, -z, -y),
        8: lambda x, y, z: (y, z, x), # (z, x, y),
        9: lambda x, y, z: (-y, -z, x), # (z, -x, -y),
        10: lambda x, y, z: (-y, z, -x), # (-z, -x, y),
        11: lambda x, y, z: (y, -z, -x), # (-z, x, -y),
        12: lambda x, y, z: (z, y, -x), # (-z, y, x),
        13: lambda x, y, z: (z, -y, x), # (z, -y, x),
        14: lambda x, y, z: (-z, y, x), # (z, y, -x),
        15: lambda x, y, z: (-z, -y, -x), # (-z, -y, -x),
        16: lambda x, y, z: (z, x, y), # (y, z, x),
        17: lambda x, y, z: (-z, x, -y), # (y, -z, -x),
        18: lambda x, y, z: (-z, -x, y), # (-y, z, -x),
        19: lambda x, y, z: (z, -x, -y), # (-y, -z, x),
        20: lambda x, y, z: (y, -x, z), # (-y, x, z),
        21: lambda x, y, z: (-y, x, z), # (y, -x, z),
        22: lambda x, y, z: (y, x, -z), # (y, x, -z),
        23: lambda x, y, z: (-y, -x, -z), # (-y, -x, -z),
    }
    try:
        new_coords = [deorientation_dict[orientation](*coord) for coord in coords]
    except TypeError:
        new_coords = deorientation_dict[orientation](*coords)
    return new_coords


def match2(scanners):
    master_list = set(scanners.pop(0))
    while scanners:
        print(f"{len(scanners) = }, {scanners.keys() = }")  #DELME
        found = False
        for scanner, coords0 in scanners.items():
            if found: break
            for orientation in range(24):
                if found: break
                coords1 = orient(coords0, orientation)
                for ref in coords1:
                    if found: break
                    coords_offset = offset(coords1, ref)
                    for ref0 in master_list:
                        if found: break
                        master_offset = offset(master_list, ref0)
                        # print(f"{master_offset = }, {coords_offset = }")  #DELME
                        n_matches = len(coords_offset & master_offset)
                        if n_matches >= 12:
                            found = True
                            print(f"{scanner = }, {ref0 = }, {orientation = }, {ref = }, {n_matches = }")
                            dref = [ref0[i] - ref[i] for i in range(len(ref))]  #DELME
                            print(f"{dref = }")  #DELME
                            nref0 = tuple(-x for x in ref0)
                            coords_to_add = offset(coords_offset, nref0)
                            master_list = master_list | coords_to_add

            if found: break
        del scanners[scanner]
    return master_list

def match3(scanners):
    loc0 = np.array([0, 0, 0], dtype='int')
    located = {0: (loc0, scanners.pop(0))}
    while scanners:
        print(f"{len(scanners) = }, {scanners.keys() = }")  #DELME
        found = False
        for scanner, coords0 in scanners.items():
            for orientation in range(24):
                coords1 = orient(coords0, orientation)
                for ref in coords1:
                    coords_offset = offset(coords1, ref)
                    for scanner_known, (dref_known, coords_known) in located.items():
                        for ref_known in coords_known:
                            coords_known_offset = offset(coords_known, ref_known)
                            n_matches = len(coords_offset & coords_known_offset)
                            if n_matches >= 12:
                                found = True
                                ref = np.array(ref)
                                ref_known = np.array(ref_known)
                                dref_local = ref_known - ref
                                dref = dref_known - ref_known + ref # dref_known - dref_local
                                print(f"{scanner = }, {scanner_known = }")  #DELME
                                print(f"{ref = }, {ref_known = }, {dref_local = }, {dref_known = }, {dref = }")  #DELME
                                located[scanner] = (dref, scanners.pop(scanner))
                                break
                            if found: break
                        if found: break
                    if found: break
                if found: break
            if found: break
    return located




    #                 for ref0 in master_list:
    #                     if found: break
    #                     master_offset = offset(master_list, ref0)
    #                     # print(f"{master_offset = }, {coords_offset = }")  #DELME
    #                     n_matches = len(coords_offset & master_offset)
    #                     if n_matches >= 12:
    #                         found = True
    #                         print(f"{scanner = }, {ref0 = }, {orientation = }, {ref = }, {n_matches = }")
    #                         dref = [ref0[i] - ref[i] for i in range(len(ref))]  #DELME
    #                         print(f"{dref = }")  #DELME
    #                         nref0 = tuple(-x for x in ref0)
    #                         coords_to_add = offset(coords_offset, nref0)
    #                         master_list = master_list | coords_to_add

    #         if found: break
    #     del scanners[scanner]
    # return master_list


def match(scanners):
    pairs = {0: (0, 0, 0)}

    # unmatched = list(scanners.keys())[1:]
    found = False
    for scanner0, coords0 in scanners.items():
        found = False
        for ref0 in coords0:
            if found: break
            coords0_offset = offset(coords0, ref0)
            for scanner1, coords1 in scanners.items():
                if scanner0 == scanner1: continue
                if found: break
                for orientation in range(24):
                    if found: break
                    coords1 = orient(coords1, orientation)
                    for ref1 in coords1:
                        if found: break
                        coords1_offset = offset(coords1, ref1)
                        n_matches = len(coords0_offset & coords1_offset)
                        if n_matches >= 12:
                            print(f"{scanner0 = }, {scanner1 = }, {ref0 = }, {orientation = }, {ref1 = }, {n_matches = }")
                            found = True
                            pairs[scanner0] = (scanner1, orientation, n_matches, ref0, ref1)
                            break
    return pairs

# def build_from_pairs(scanners, pairs):
#     master_list = set(scanners[0])
#     locations = {0: (0, 0, 0)}
#     # for 


scanners = parse_input('test.txt')
pairs = match(scanners)
located = match3(scanners)

print([(key, x[0]) for key, x in located.items()])
# master_list = match2(scanners)
# print(f"{len(master_list) = }")

# master_list_ref = set()
# with open('test_ans.txt') as f:
#     for line in f:
#         coord = tuple(map(int, line.strip().split(',')))
#         master_list_ref.add(coord)

# ref0 = np.array(pairs[0][3])
# ref1 = np.array(pairs[0][4])

# ref = np.array([-554, -779,  293], dtype='int')
# ref_known = np.array([-466, -666, -811], dtype='int')
# dref_local = np.array([   88,   113, -1104], dtype='int')
# dref_known = np.array([   68, -1246,   -43], dtype='int')
# dref = np.array([  156, -1133, -1147], dtype='int')

ref = np.array([-554, -779,  293], dtype='int')
ref_known = np.array([-466, -666, -811], dtype='int')
dref_local = np.array([   88,   113, -1104], dtype='int')
dref_known = np.array([ -68, 1246,   43], dtype='int')
dref = np.array([-156, 1133, 1147], dtype='int')

dref4 = np.array([-20,-1133,1061], dtype='int')