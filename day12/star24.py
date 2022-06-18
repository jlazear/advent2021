class Node:
    def __init__(self, id, nodes):
        self.connections = []
        self.id = id
        self.nodes = nodes
        self.nodes[id] = self
        self.small = id.islower()
    
    def connect(self, id):
        try:
            node = self.nodes[id]
        except KeyError:
            node = Node(id, self.nodes)
        self.connections.append(node)
        node.connections.append(self)

    def __repr__(self):
        return "<Node {}, connections = {}>".format(self.id, [c.id for c in self.connections])
    
def read_input(fname='input.txt'):
    nodes = {}
    with open(fname) as f:
        for line in f:
            node1_id, node2_id = line.strip().split('-')
            try:
                node1 = nodes[node1_id]
            except KeyError:
                node1 = Node(node1_id, nodes)
            node1.connect(node2_id)
    return nodes

def dfs(node_id, end_id, nodes, visited, path, paths, twice):
    # print(f"{node_id} {twice} ", [x.id for x in visited])  #DELME
    node = nodes[node_id]
    adjacent = node.connections
    for next in adjacent:
        next_twice = twice
        if next in visited:
            if twice or (next.id in ('start', 'end')):
                continue
            else:
                next_twice = 1
        next_visited = visited + [next] if next.small else visited
        next_path = path + [next]
        if next.id == end_id:
            paths.append(next_path)
        paths = dfs(next.id, end_id, nodes, next_visited, next_path, paths, next_twice)
    return paths
            

def format_path(path):
    return '-'.join([node.id for node in path])


print("---- test.txt ----")
nodes = read_input('test.txt')
paths = dfs('start', 'end', nodes, [nodes['start']], [nodes['start']], [], 0)

for path in paths:
    print(format_path(path))

print("number of paths = ", len(paths))


print("---- input.txt ----")
nodes = read_input('input.txt')
paths = dfs('start', 'end', nodes, [nodes['start']], [nodes['start']], [], 0)

# for path in paths:
#     print(format_path(path))

print("number of paths = ", len(paths))

