import sys

input = []

def handle(line):
    if line != "":
        input.append(line)

def line_without_newline(line):
    return line[:-1]

def point_pairs(points):
    pairs = []
    for i in range(len(points)):
        j = i + 1
        while(j < len(points)):
            pairs.append([points[i],points[j]])
            j += 1
    return pairs

lastline='a'

for line in sys.stdin:
    if(line[:-1] == '' and lastline == ''):
        print("should be ending stdin")
        break
    else:
        handle(line_without_newline(line))
        lastline = line[:-1]

for line in input:
    print(line)

max_row = len(input)
max_col = len(input[0])

antennae = {}
used_points = []

def in_bounds(point):
    row = point[0]
    col = point[1]
    return row >= 0 and col >= 0 and row < max_row and col < max_col

def projected_points(points):
    point1 = points[0]
    point2 = points[1]
    cheb_distance = max(abs(point1[0] - point2[0]),abs(point1[1] - point2[1]))

    direction_1_diff = [point1[0] - point2[0], point1[1] - point2[1]]
    direction_2_diff = [point2[0] - point1[0], point2[1] - point1[1]]

    num_to_project = int(60 / cheb_distance) + 1

    current1 = point1
    current2 = point2
    result = [point1, point2]
    for i in range(num_to_project):
        current1 = project_point(current1, direction_1_diff)
        current2 = project_point(current2, direction_2_diff)
        result.append(current1)
        result.append(current2)
    return result

def project_point(point, diff):
    return[point[0] + diff[0], point[1] + diff[1]]

for row in range(len(input)):
    for col in range(len(input[0])):
        value = input[row][col]
        if value != ".":
            used_points.append([row, col])
            if value in antennae:
                antennae[value].append([row, col])
            else:
                antennae[value] = [[row, col]]

antinodes = []
num_antinodes = 0
for n in antennae:
    n_pairs = point_pairs(antennae[n])
    for pair in n_pairs:
        projections = projected_points(pair)
        for projection in projections:
            if in_bounds(projection) and projection not in antinodes:
                antinodes.append(projection)
print(f"antinodes {len(antinodes)}")



            