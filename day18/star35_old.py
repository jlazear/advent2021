class Node:
    def __init__(self, value, parent):
        self.value = value
        self.parent = parent

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
        return f"[^{self.parent}: {self.left},{self.right}]"

    def descend_right(self):
        if isinstance(self.right, int):
            return self
        return self.right.descend_right()

    def descend_left(self):
        if isinstance(self.left, int):
            return self
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
            if isinstance(parent.left, int):
                return parent
            else:
                return parent.left.descend_right()
        else:
            return parent.find_next_left()                

    def find_next_right(self):
        parent = self.parent
        if parent is None:
            return None
        if parent.left == self:
            if isinstance(parent.right, int):
                return parent
            else:
                return parent.right.descend_left()
        else:
            return parent.find_next_right()

    def _explode(self):
        if not (isinstance(self.left, int) and isinstance(self.right, int)):
            raise Exception(f"Cannot explode this node (not a leaf): {self}")
        if self.depth < self.explode_depth:
            raise Exception(f"Cannot explode this node (too shallow): {self}")

        if (left_pair := self.find_next_left()):
            left_pair.left += self.left
        if (right_pair := self.find_next_right()):
            print(f"{right_pair = }\n {right_pair.right = }\n {self.right = }")  #DELME
            right_pair.right += self.right

        if self.parent.left == self:
            self.parent.left = 0
        else:
            self.parent.right = 0
        return self.find_root()

    def explodeable(self):
        return (isinstance(self.left, int) and (isinstance(self.right, int) and self.depth >= self.explode_depth))

    def explode(self):
        print(f"explode in pair {self}, depth: {self.depth}, explodeable: {self.explodeable()}")  #DELME
        if self.explodeable():
            self._explode()
            return True
        elif isinstance(self.left, Pair) and self.left.explode():
            return True
        elif isinstance(self.right, Pair) and self.right.explode():
            return True
        else:
            return False

     

def parse_number(number):
    if isinstance(number, int):
        return number
    left = parse_number(number[0])
    right = parse_number(number[1])
    p = Pair(left, right)
    if isinstance(left, Pair):
        left.parent = p
    if isinstance(right, Pair):
        right.parent = p
    
    return p

def assign_depths(p, depth=0):
    if isinstance(p, int):
        return
    p.depth = depth
    assign_depths(p.left, depth+1)
    assign_depths(p.right, depth+1)
    


# [[[[[9,8],1],2],3],4] becomes [[[[0,9],2],3],4]
pe0 = parse_number([[[[[9,8],1],2],3],4])
assign_depths(pe0)
# pe0sub = pe0.left.left.left.left

print("[[[[[9,8],1],2],3],4] becomes [[[[0,9],2],3],4]")
# print(pe0sub._explode())
print(pe0.explode())
print(pe0)

# [7,[6,[5,[4,[3,2]]]]] becomes [7,[6,[5,[7,0]]]]
pe1 = parse_number([7,[6,[5,[4,[3,2]]]]])
assign_depths(pe1)
# pe1sub = pe1.right.right.right.right

print("[7,[6,[5,[4,[3,2]]]]] becomes [7,[6,[5,[7,0]]]]")
# print(pe1sub._explode())
print(pe1.explode())
print(pe1)


# [[6,[5,[4,[3,2]]]],1] becomes [[6,[5,[7,0]]],3]

pe2 = parse_number([[6,[5,[4,[3,2]]]],1])
assign_depths(pe2)
# pe2sub = pe2.left.right.right.right
print("[[6,[5,[4,[3,2]]]],1] becomes [[6,[5,[7,0]]],3]")
# print(pe2sub._explode())
print(pe2.explode())
print(pe2)

# [[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]] becomes [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]

pe3 = parse_number([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]])
assign_depths(pe3)
print("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]] becomes [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")
print(pe3.explode())
print(pe3)