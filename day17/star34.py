import numpy as np

# this should work but some bug... can't be bothered to fix it
# def nx_range(v, low=185, high=221):
#     n_min = np.ceil(0.5*(v + 0.5)*(1 - np.sqrt(1 - 2*low/(v + 0.5)**2)))
#     n_max = np.floor(0.5*(v + 0.5)*(1 - np.sqrt(1 - 2*high/(v + 0.5)**2)))
#     return n_min, n_max

# def ny_range(v, low=-122, high=-74):
#     n_max = np.floor((v - 0.5) + np.sqrt((v - 0.5)**2 - 2*low))
#     n_min = np.ceil((v - 0.5) + np.sqrt((v - 0.5)**2 - 2*high))
#     return n_min, n_max

# def overlap(nx1, nx2, ny1, ny2):
#     return not ((nx2 < ny1) or (ny2 < nx1))

# def valid(vx, vy, xlow=185, xhigh=221, ylow=-122, yhigh=-74):
#     nx1, nx2 = nx_range(vx, low=xlow, high=xhigh)
#     ny1, ny2 = ny_range(vy, low=ylow, high=yhigh)
#     if np.isnan(nx1) and np.isnan(nx2):
#         return False
#     if np.isnan(nx2):
#         nx2 = np.inf
#     else:
#         nx2 = int(nx2)
#     if ny2 < ny1:
#         return False
    
#     return overlap(int(nx1), nx2, int(ny1), int(ny2))

def iterate(x, y, vx, vy):
    newx = x + vx
    newy = y + vy
    vx = max(0, vx - 1)
    vy = vy - 1
    return newx, newy, vx, vy

def hit(x, y, xlow=185, xhigh=221, ylow=-122, yhigh=-74):
    if (x >= xlow) and (x <= xhigh) and (y >= ylow) and (y <= yhigh):
        return True
    else:
        return False

def miss(x, y, vx, vy, xlow=185, xhigh=221, ylow=-122, yhigh=-74):
    if (x < xlow) and vx == 0:
        return True
    if (x > xhigh):
        return True
    if (y < ylow):
        return True
    return False

def check_valid(vx, vy, xlow=185, xhigh=221, ylow=-122, yhigh=-74):
    x, y = 0, 0
    n = 0
    while not miss(x, y, vx, vy, xlow=xlow, xhigh=xhigh, ylow=ylow, yhigh=yhigh):
        if hit(x, y, xlow=xlow, xhigh=xhigh, ylow=ylow, yhigh=yhigh):
            return True
        x, y, vx, vy = iterate(x, y, vx, vy)
        n += 1
    return False

valids = []
for vx in range(250):
    for vy in range(-150, 500):
        if check_valid(vx, vy):
            valids.append((vx, vy))

print(f"{len(valids) = }")