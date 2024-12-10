import sys


def line_without_newline(line):
    return line[:-1]

input = []

def handle(line):
    if(line != ""):
        input.append([int(x) for x in line ])    


lastline='a'
for line in sys.stdin:
    if(line[:-1] == '' and lastline == ''):
        print("should be ending stdin")
        break
    else:
        handle(line_without_newline(line))
        lastline = line[:-1]

max_row = len(input)
max_col = len(input[0])
def in_bounds(row, col):
    return row >= 0 and col >= 0 and row < max_row and col < max_col

def possible_steps(row, col):
    possible = []
    if in_bounds(row - 1, col):
        val = input[row - 1][col] - input[row][col]
        if val == 1:
            possible.append([row - 1, col])

    if in_bounds(row + 1, col):
        val = input[row + 1][col] - input[row][col]
        if val == 1:
            possible.append([row + 1, col])
    
    if in_bounds(row, col + 1):
        val = input[row][col + 1] - input[row][col]
        if val == 1:
            possible.append([row, col + 1])
    
    if in_bounds(row, col - 1):
        val = input[row][col - 1] - input[row][col]
        if val == 1:
            possible.append([row, col - 1])
    return possible

destinations = []
for i in range(max_row):
    for j in range(max_col):
        if input[i][j] == 9:
            destinations.append([i, j])

def can_reach(start_r, start_c, end_r, end_c, visited):
    current = [start_r, start_c]
    visited.append(current)
    paths = [x for x in possible_steps(current[0], current[1]) if x not in visited]
    if len(paths) == 0:
        return 0
    results_of_paths = 0
    for path in paths:
        if path == [end_r, end_c]:
            return 1
        results_of_paths += can_reach(path[0], path[1], end_r, end_c, visited)
    return results_of_paths > 0



def num_paths_from_to(start_r, start_c, end_r, end_c, visited):
    current = [start_r, start_c]
    #print(f"{current} {[end_r, end_c] in visited}")
    #visited.append(current)
    paths = [x for x in possible_steps(current[0], current[1]) if x not in visited]
    if len(paths) == 0:
        return 0
    num_paths = 0
    for path in paths:
        if path == [end_r, end_c]:
            return 1
        num_paths += num_paths_from_to(path[0], path[1], end_r, end_c, visited)
    return num_paths
        


def check_path(row, col):
    score = 0
    for dest in destinations:
        if can_reach(row, col, dest[0], dest[1], []):
            score += 1
    return score

def check_path_2(row, col):
    rating = 0
    for dest in destinations:
        rating += num_paths_from_to(row, col, dest[0], dest[1], [])
    return rating

#print(can_reach(0,3,6,0,[]))
answer = 0
for i in range(max_row):
    for j in range(max_col):
        if input[i][j] == 0:
            answer += check_path(i, j)
print(answer)

answer = 0
for i in range(max_row):
    for j in range(max_col):
        if input[i][j] == 0: 
            answer += check_path_2(i, j)
print(answer)
