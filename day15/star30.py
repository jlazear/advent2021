import math
import heapq

def parse_input(fname='input.txt'):
    risks = []
    with open(fname) as f:
        for line in f:
            risk_row = [int(x) for x in line.strip()]
            risks.append(risk_row)
    return risks

def get_neighbors(node, len_i, len_j, n_tile_i=5, n_tile_j=5):
    neighbors = []
    i, j = node
    if i > 0:
        neighbors.append((i-1, j))
    if j > 0:
        neighbors.append((i, j-1))
    if i < n_tile_i*len_i - 1:
        neighbors.append((i+1, j))
    if j < n_tile_j*len_j - 1:
        neighbors.append((i, j+1))
    return neighbors

def get_risk(node, risks):
    i, j = node
    len_i = len(risks)
    len_j = len(risks[0])

    base_i = i % len_i
    base_j = j % len_j

    tile_i = math.floor(i/len_i)
    tile_j = math.floor(j/len_j)

    mod_risk = risks[base_i][base_j] + tile_i + tile_j
    mod_risk = (mod_risk % 10) + (1 if (mod_risk >= 10) else 0)
    return mod_risk


def dijkstra(start, end, risks, n_tile_i=5, n_tile_j=5):
    len_i = len(risks)
    len_j = len(risks[0])
    INFINITY = len_i * len_j * 9 * n_tile_i * n_tile_j
    neighbors = lambda node: get_neighbors(node, len_i, len_j)
    
    total_risks = {(i, j): INFINITY for i in range(len_i*n_tile_i) for j in range(len_j*n_tile_j)}
    total_risks[start] = 0
    
    # previous = {(i, j): None for i in range(len(risks)) for j in range(len(risks))}  # don't need path
    visited = set()

    queue = [(0, start)]
    while queue:
        risk, node = heapq.heappop(queue)  # pops lowest risk element
        visited.add(node)
        if node == end:
            return total_risks

        for neighbor in neighbors(node):
            if neighbor not in visited:
                risk = get_risk(neighbor, risks)
                old_total_risk = total_risks[neighbor]
                new_total_risk = total_risks[node] + risk
                if new_total_risk < old_total_risk:
                    heapq.heappush(queue, (new_total_risk, neighbor))
                    total_risks[neighbor] = new_total_risk

    return total_risks
            

risks = parse_input('input.txt')

start = (0, 0)
n_tile_i = 5
n_tile_j = 5
end = (len(risks)*n_tile_i - 1, len(risks[0])*n_tile_j - 1)

total_risks = dijkstra(start, end, risks)
min_risk = total_risks[end]
print(f"{min_risk = }")