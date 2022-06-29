import warnings
import copy
import sys

class Node:
    def __init__(self, name, neighbors=[], occupant=None, occupiable=True):
        self.name = name
        self.neighbors = set(neighbors)
        self.occupant = occupant
        self.occupiable = occupiable
    
    def connect(self, neighbor):
        self.neighbors.add(neighbor)
        neighbor.neighbors.add(self)

    def __str__(self):
        neighbor_str = ', '.join([neighbor.name for neighbor in self.neighbors])
        occupiable = '' if self.occupiable else '*'
        if self.occupant:
            return f"Node({self.name}{occupiable} ({self.occupant.name}) -> [{neighbor_str}])"
        else:
            return f"Node({self.name}{occupiable} -> [{neighbor_str}])"
    
    def __repr__(self):
        return self.__str__()

class Amphipod:
    cost_dict = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
    def __init__(self, name, type, location, node_dict, moved=0, steps=0):
        self.name = name
        self.type = type
        self.location = node_dict[location]
        self.location.occupant = self
        self.node_dict = node_dict
        self.moved = moved
        self.stepcost = self.cost_dict[type]
        self.steps = steps

        RA0 = node_dict['RA0']
        RA1 = node_dict['RA1']
        RB0 = node_dict['RB0']
        RB1 = node_dict['RB1']
        RC0 = node_dict['RC0']
        RC1 = node_dict['RC1']
        RD0 = node_dict['RD0']
        RD1 = node_dict['RD1']
        self.home_dict = {'A': [RA0, RA1],
                          'B': [RB0, RB1],
                          'C': [RC0, RC1],
                          'D': [RD0, RD1]}
        self.homes = self.home_dict[type]

    def __str__(self):
        return f"Amph({self.name} @ {self.location.name}, {self.moved}/2)"

    def __repr__(self):
        return self.__str__()

    def available(self):
        locations = {}
        visited = set()
        neighbors = [(neighbor, 1) for neighbor in self.location.neighbors if not neighbor.occupant]
        while neighbors:
            neighbor, steps = neighbors.pop()
            visited.add(neighbor)
            if neighbor.occupiable:
                if self.moved < 1:
                    locations[neighbor] = steps
                elif self.moved == 1 and neighbor in self.homes:
                    locations[neighbor] = steps
            new_neighbors = [(new_neighbor, steps+1) for new_neighbor in neighbor.neighbors
                                                     if not new_neighbor.occupant and new_neighbor not in visited]
            neighbors.extend(new_neighbors)
        if self.moved:
            if self.homes[1] in locations and self.homes[0] in locations:
                del locations[self.homes[0]]
        return locations

    def move(self, target):
        if not isinstance(target, Node):
            target = self.node_dict[target]
        available = self.available()
        
        if self.moved >= 2:
            warnings.warn(f"{self} has moved too many times already")
            return False
        if target not in available:
            warnings.warn(f"Invalid move of {self} from {self.location} to {target}")
            return False
        
        target.occupant = self
        self.location.occupant = None
        self.location = target
        self.steps += available[target]
        self.moved += 1
        return True

class State:
    def __init__(self, node_dict, amphipods):
        self.node_dict = node_dict
        self.amphipods = amphipods

    def __getitem__(self, key):
        return self.amphipods[key]

    def state_tuple(self):
        return tuple((name, amphipod.moved, amphipod.location.name) for name, amphipod in self.amphipods.items())

    def is_equal(self, other):
        return hash(self.state_tuple()) == hash(other.state_tuple())

    def get_dead(self):
        return [name for name, amphipod in self.amphipods.items() if amphipod.moved >= 2]

    def copy(self):
        return copy.deepcopy(self)

    def movable(self):
        return [amphipod for amphipod in self.amphipods.values() if amphipod.moved < 2]

    def next_moves(self, include_state=True):
        next_moves = []
        for amphipod in self.movable():
            for target in amphipod.available():
                if include_state:
                    next_moves.append((amphipod.name, target.name, self))
                else:
                    next_moves.append((amphipod, target))
        return next_moves

    def success(self):
        for amphipod in self.amphipods.values():
            if amphipod.location not in amphipod.homes:
                return False
        return True

    def cost(self):
        return sum([amphipod.stepcost*amphipod.steps for amphipod in self.amphipods.values()])


def make_map():
    H0 = Node('H0')
    H1 = Node('H1')
    H2 = Node('H2', occupiable=False)
    H3 = Node('H3')
    H4 = Node('H4', occupiable=False)
    H5 = Node('H5')
    H6 = Node('H6', occupiable=False)
    H7 = Node('H7')
    H8 = Node('H8', occupiable=False)
    H9 = Node('H9')
    H10 = Node('H10')
    RA0 = Node('RA0')
    RA1 = Node('RA1')
    RB0 = Node('RB0')
    RB1 = Node('RB1')
    RC0 = Node('RC0')
    RC1 = Node('RC1')
    RD0 = Node('RD0')
    RD1 = Node('RD1')
    node_dict = {node.name: node for node in [H0, H1, H2, H3, H4, H5, H6, H7, H8, H9, H10, 
                                              RA0, RA1, RB0, RB1, RC0, RC1, RD0, RD1]}

    hallway = [H0, H1, H2, H3, H4, H5, H6, H7, H8, H9, H10]
    for i in range(len(hallway))[:-1]:
        Ha = hallway[i]
        Hb = hallway[i+1]
        Ha.connect(Hb)

    RA0.connect(RA1)
    RB0.connect(RB1)
    RC0.connect(RC1)
    RD0.connect(RD1)

    H2.connect(RA0)
    H4.connect(RB0)
    H6.connect(RC0)
    H8.connect(RD0)
    return node_dict

def make_amphipods(node_dict, a0='RA0', a1='RB1', b0='RA1', b1='RC0', c0='RB0', c1='RD1', d0='RC1', d1='RD0'):
    A0 = Amphipod('A0', 'A', a0, node_dict)
    A1 = Amphipod('A1', 'A', a1, node_dict)
    B0 = Amphipod('B0', 'B', b0, node_dict)
    B1 = Amphipod('B1', 'B', b1, node_dict)
    C0 = Amphipod('C0', 'C', c0, node_dict)
    C1 = Amphipod('C1', 'C', c1, node_dict)
    D0 = Amphipod('D0', 'D', d0, node_dict)
    D1 = Amphipod('D1', 'D', d1, node_dict)
    amphipods = {amphipod.name: amphipod for amphipod in [A0, A1, B0, B1, C0, C1, D0, D1]}
    return amphipods

def make_state(a0='RA0', a1='RB1', b0='RA1', b1='RC0', c0='RB0', c1='RD1', d0='RC1', d1='RD0'):
    node_dict = make_map()
    amphipods = make_amphipods(node_dict, a0=a0, a1=a1, b0=b0, b1=b1, c0=c0, c1=c1, d0=d0, d1=d1)
    state = State(node_dict, amphipods)
    return state

def print_map(node_dict):
    base_map = (
"""#############
#...........#
###.#.#.#.###
  #.#.#.#.#
  #########""")
    base_list = [[c for c in line] for line in base_map.split('\n')]

    locs = {'H0': (1, 1),
            'H1': (1, 2),
            'H2': (1, 3),
            'H3': (1, 4),
            'H4': (1, 5),
            'H5': (1, 6),
            'H6': (1, 7),
            'H7': (1, 8),
            'H8': (1, 9),
            'H9': (1, 10),
            'H10': (1, 11),
            'RA0': (2, 3),
            'RA1': (3, 3),
            'RB0': (2, 5),
            'RB1': (3, 5),
            'RC0': (2, 7),
            'RC1': (3, 7),
            'RD0': (2, 9),
            'RD1': (3, 9)
            }

    for name, node in node_dict.items():
        if node.occupant:
            i, j = locs[name]
            base_list[i][j] = node.occupant.type
        if not node.occupiable:
            i, j = locs[name]
            base_list[i][j] = 'o'

    view = '\n'.join([''.join([c for c in line]) for line in base_list])
    return view, base_list

state = make_state()

moves = [('D1', 'H9'),
         ('B1', 'H3'),
         ('C1', 'H5'),
         ('D1', 'RD1'),
         ('D0', 'RD0'),
         ('C1', 'RC1'),
         ('C0', 'RC0'),
         ('A1', 'H5'),
         ('B1', 'RB1'),
         ('A0', 'H1'),
         ('B0', 'RB0'),
         ('A0', 'RA1'),
         ('A1', 'RA0')]

for amphipod, target in moves:
    state[amphipod].move(target)