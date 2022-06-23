import math
from collections import deque

class Node:
    split_threshold = 10

    def __init__(self, value, parent=None, depth=0):
        self.value = value
        self.parent = parent
        self.depth = depth

    def __repr__(self):
        return f"Node({self.value})"

    def __str__(self):
        return str(self.value)

    def __add__(self, other):
        return self.value + other.value

    def __iadd__(self, other):
        self.value += other.value
        return self

    def splittable(self):
        return (self.value >= self.split_threshold)

    def split(self):
        if not self.splittable():
            return False
        left = Node(math.floor(self.value/2), depth=self.depth+1)
        right = Node(math.ceil(self.value/2), depth=self.depth+1)
        p = Pair(left, right, self.parent, self.depth)
        left.parent = p
        right.parent = p
        
        parent = self.parent
        if parent.left == self:
            parent.left = p
        else:
            parent.right = p
        return True
    
    def magnitude(self):
        return self.value


class Pair:
    explode_depth = 4

    def __init__(self, left, right, parent=None, depth=0):
        self.left = left
        self.right = right
        self.parent = parent
        self.depth = depth

    def __str__(self) -> str:
        return f"[{self.left},{self.right}]"

    def __repr__(self) -> str:
        return self.__str__()

    def descend_right(self):
        if isinstance(self.right, Node):
            return self.right
        return self.right.descend_right()

    def descend_left(self):
        if isinstance(self.left, Node):
            return self.left
        return self.left.descend_left()

    def find_root(self):
        if self.parent is None:
            return self
        return self.parent.find_root()

    def find_next_left(self):
        parent = self.parent
        if parent is None:
            return None
        if parent.right == self:
            if isinstance(parent.left, Node):
                return parent.left
            else:
                return parent.left.descend_right()
        else:
            return parent.find_next_left()                

    def find_next_right(self):
        parent = self.parent
        if parent is None:
            return None
        if parent.left == self:
            if isinstance(parent.right, Node):
                return parent.right
            else:
                return parent.right.descend_left()
        else:
            return parent.find_next_right()

    def _explode(self):
        if not (isinstance(self.left, Node) and isinstance(self.right, Node)):
            raise Exception(f"Cannot explode this node (not a leaf): {self}")
        if self.depth < self.explode_depth:
            raise Exception(f"Cannot explode this node (too shallow): {self}")

        if (left_pair := self.find_next_left()):
            left_pair += self.left
        if (right_pair := self.find_next_right()):
            right_pair += self.right

        if self.parent.left == self:
            self.parent.left = Node(0, self.parent, self.depth)
        else:
            self.parent.right = Node(0, self.parent, self.depth)
        return self.find_root()

    def explodeable(self):
        return (isinstance(self.left, Node) and (isinstance(self.right, Node) and self.depth >= self.explode_depth))

    def explode(self):
        if self.explodeable():
            self._explode()
            return True
        elif isinstance(self.left, Pair) and self.left.explode():
            return True
        elif isinstance(self.right, Pair) and self.right.explode():
            return True
        else:
            return False

    def split(self):
        if self.left.split():
            return True
        elif self.right.split():
            return True
        else:
            return False

    def reduce(self):
        if self.parent is not None:
            return False
        
        repeat_split = True
        while repeat_split:
            repeat_explode = True
            while self.explode():
                pass
            repeat_split = self.split()
        return True

    def magnitude(self):
        return 3*self.left.magnitude() + 2*self.right.magnitude()

     
def parse_number(number):
    p = _parse_number(number)
    assign_depths(p)
    return p

def _parse_number(number):
    if isinstance(number, int):
        return Node(number)
    left = _parse_number(number[0])
    right = _parse_number(number[1])
    p = Pair(left, right)
    left.parent = p
    right.parent = p
    
    return p

def assign_depths(p, depth=0):
    p.depth = depth
    if isinstance(p, Pair):
        assign_depths(p.left, depth+1)
        assign_depths(p.right, depth+1)
    
def sum_pairs(p1, p2):
    p = Pair(p1, p2)
    p1.parent = p
    p2.parent = p
    assign_depths(p)
    return p

ps = deque()
with open('input.txt') as f:
    for line in f:
        p = parse_number(eval(line.strip()))
        ps.append(p)

p1 = ps.popleft()
while ps:
    p2 = ps.popleft()
    p1 = sum_pairs(p1, p2)
    p1.reduce()

print(f"{p1.magnitude() = }")