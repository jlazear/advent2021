with open('input.txt') as f:
    fish = list(map(int, f.readline().split(',')))

day = 0
day_max = 80

while day < day_max:
    num_fish = len(fish)
    for i in range(num_fish):
        age = fish[i]
        if age == 0:
            fish[i] = 6
            fish.append(8)
        else:
            fish[i] -= 1
    day += 1

print(len(fish))
