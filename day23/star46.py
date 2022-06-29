# import warnings
# import copy
import sys
from functools import cache


def room_complete(room, expected):
    return sum((spot == expected for spot in room)) == len(room)

def room_empty(room):
    return sum((spot is None for spot in room)) == len(room)

def room_semicomplete(room, expected):
    return sum((spot in (None, expected) for spot in room)) == len(room)

def state_complete(state):
    return sum([room_complete(state[1], 'A'),
                room_complete(state[2], 'B'),
                room_complete(state[3], 'C'),
                room_complete(state[4], 'D')]) == 4

def room_receivable(room, expected):
    return (sum([x in (None, expected) for x in room]) == len(room) 
            and not room_complete(room, expected))

room_map = {'A': 1,
            'B': 2,
            'C': 3,
            'D': 4}
room_map_rev = {value: key for key, value in room_map.items()}

entrance_dict = {'A': 2,
                 'B': 4,
                 'C': 6,
                 'D': 8}

cost_dict = {'A': 1,
             'B': 10,
             'C': 100,
             'D': 1000}


def path_to_room_clear(state, hall_index):
    amphipod = state[0][hall_index]  # A, B, C, or D
    room = state[room_map[amphipod]]
    if not room_receivable(room, amphipod):  # destination room must be clear for hallway amphipod to move
        return False
    
    entrance_index = entrance_dict[amphipod]
    if hall_index < entrance_index:
        return sum([state[0][i] is None for i in range(hall_index+1, entrance_index+1)]) == entrance_index - hall_index
    else:
        return sum([state[0][i] is None for i in range(entrance_index, hall_index)]) == hall_index - entrance_index


def movable(state):
    hall, roomA, roomB, roomC, roomD = state

    for i, amphipod in enumerate(hall):
        if amphipod is None:
            continue
        if path_to_room_clear(state, i):
            return i  # always move amphipod into home if available, doesn't matter order
    
    moves = []

    for i, room in enumerate(state[1:]):
        if not (room_complete(room, room_map_rev[i+1]) or room_empty(room) or room_semicomplete(room, room_map_rev[i+1])):
            moves.append(i+1)
        
    return moves

def next_moves_from_room(state, room_index):
    hall = state[0]
    entrance_index = room_index*2
    valid = []
    index = entrance_index-1
    while index >= 0 and not hall[index]:
        if index not in (2, 4, 6, 8):
            valid.append(index)
        index -= 1

    index = entrance_index + 1
    while index < len(hall) and not hall[index]:
        if index not in (2, 4, 6, 8):
            valid.append(index)
        index += 1
    valid = sorted(valid)
    return valid

def move_from_hall(state, hall_index):
    new_state = list(state)
    amphipod = state[0][hall_index]
    room_index = room_map[amphipod]
    
    # construct new state
    new_room = list(state[room_index])
    last_none = max([i for i, x in enumerate(new_room) if x is None])
    new_room[last_none] = amphipod
    
    new_hall = list(state[0])
    new_hall[hall_index] = None

    new_state[0] = tuple(new_hall)
    new_state[room_index] = tuple(new_room)
    new_state = tuple(new_state)

    # calculate cost
    entrance_index = entrance_dict[amphipod]
    hall_dist = abs(entrance_index - hall_index)
    room_dist = last_none + 1
    cost = (hall_dist + room_dist) * cost_dict[amphipod]
    return new_state, cost

def move_from_room(state, room_index, hall_index):
    new_state = list(state)
    room = state[room_index]
    amphipod_index = [i for i, x in enumerate(room) if x is not None][0]
    amphipod = room[amphipod_index]

    # construct new state
    new_room = list(state[room_index])
    new_room[amphipod_index] = None
    
    new_hall = list(state[0])
    new_hall[hall_index] = amphipod

    new_state[0] = tuple(new_hall)
    new_state[room_index] = tuple(new_room)
    new_state = tuple(new_state)

    # calculate cost
    entrance_index = room_index*2
    hall_dist = abs(entrance_index - hall_index)
    room_dist = amphipod_index + 1
    cost = (hall_dist + room_dist) * cost_dict[amphipod]
    return new_state, cost

i = 0  #DELME
@cache
def dfs(state, cost=0):
    if state_complete(state):
        print(f"FOUND TERMINAL STATE with {cost = }")  #DELME
        return cost
    
    moves = movable(state)
    if isinstance(moves, int):
        new_state, new_cost = move_from_hall(state, moves)
        return dfs(new_state, cost + new_cost)
    else:
        costs = []
        for room_index in moves:
            for hall_index in next_moves_from_room(state, room_index):
                new_state, new_cost = move_from_room(state, room_index, hall_index)
                costs.append(dfs(new_state, new_cost + cost))
        if costs:
            return min(costs)
    return sys.maxsize

hall = tuple(None for _ in range(11))
roomA = ('A', 'D', 'D', 'B')
roomB = ('C', 'C', 'B', 'A')
roomC = ('B', 'B', 'A', 'D')
roomD = ('D', 'A', 'C', 'C')
state = (hall, roomA, roomB, roomC, roomD)

min_cost = dfs(state)
print(f"{min_cost = }")