import sys

input = []


def line_without_newline(line):
    return line[:-1]

def handle(line):
    if(line == ""):
        return 0
    input.append([x for x in line])
    return 1

lastline='a'
for line in sys.stdin:
    if(line[:-1] == '' and lastline == ''):
        print("should be ending stdin")
        break
    else:
        handle(line_without_newline(line))
        lastline = line[:-1]


max_row = len(input) - 1
max_col = len(input[0]) - 1

def in_bounds(row, col):
    return row >= 0 and col >= 0 and row <= max_row and col <= max_col

def get_adjacent(row, col):
    return [[row - 1, col],
            [row + 1, col],
            [row, col -1],
            [row, col + 1]]

fields = []
visited = []

def get_field(row, col):
    veg = input[row][col]
    to_check = [[row, col]]
    field = []
    while len(to_check) > 0:
        current = to_check.pop(0)
        if input[current[0]][current[1]] == veg and not current in field and not current in visited:
            field.append(current)
            visited.append(current)
            current_adj = get_adjacent(current[0],current[1])
            for point in current_adj:
                if point not in field and in_bounds(point[0], point[1]):
                    to_check.append(point)
                    
    return field


#Iteration to get fields
for i in range(len(input)):
    for j in range(len(input[0])):
        if [i,j] not in visited:
            fields.append(get_field(i, j))

def get_square_corners(point):
    return [[point[0] - .5, point[1] + .5],
    [point[0] + .5, point[1] + .5],
    [point[0] - .5, point[1] - .5],
    [point[0] + .5, point[1] - .5]]

def hash_list(list):
    return f"{list[0]}-{list[1]}"

def dehash_list(str):
    return [int(x) for x in str.split("-")]

def get_num_sides(field):
    centered_field = [[point[0] + .5, point[1] + .5] for point in field]
    corner_counts = {}
    for point in centered_field:
        corners = get_square_corners(point)
        for corner in corners:
            key = hash_list(corner)
            if key in corner_counts:
                corner_counts[key] += 1
            else:
                corner_counts[key] = 1
    num_sides = 0
    for key in corner_counts:
        if corner_counts[key] % 2 == 1:
            num_sides += 1
    return num_sides

answer = 0

for field in fields:
    print(input[field[0][0]][field[0][1]])
    print(field)
    print(len(field))
    num_sides = get_num_sides(field)
    print(num_sides)
    answer += len(field) * get_num_sides(field)

print(answer)
    
