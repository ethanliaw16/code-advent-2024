import sys

input = []
visited = []
directions = ["left","up","right","down"]
next_direction = {"left":"up", "up":"right", "right":"down", "down":"left"}

def without_nth_item(n, lst):
    return lst[:n] + lst[n+1:]

def line_without_newline(line):
    return line[:-1]

def handle(line):
    if(line == ""):
        return 0
    input.append(line)
    visited.append([[] for x in line])
    return 1

lastline='a'
for line in sys.stdin:
    if(line[:-1] == '' and lastline == ''):
        print("should be ending stdin")
        break
    else:
        handle(line_without_newline(line))
        lastline = line[:-1]

empty_visited = visited
start_row = 0
start_col = 0
for i in range(len(input)):
    if input[i].find("^") != -1:
        start_row = i
        start_col = input[i].find("^")

def left_area(row, column):
    return row < 0 or row > len(input) - 1 or column < 0 or column > len(input[0]) - 1

print(f"start at row {start_row} col {start_col}")

def travel_right(row, column):
    current_row = row
    current_col = column
    while not left_area(current_row, current_col) and input[current_row][current_col] != "#":
        if "right" in visited[current_row][current_col]:
            return [current_row, current_col, "loop"]
        visited[current_row][current_col].append("right")
        if current_col == len(input[0]) - 1:
            return [current_row, current_col + 1]
        current_col += 1
    current_col -= 1
    return [current_row, current_col]

def travel_up(row, column):
    current_row = row
    current_col = column
    while not left_area(current_row, current_col) and input[current_row][current_col] != "#":
        if "up" in visited[current_row][current_col]:
            return [current_row, current_col, "loop"]
        visited[current_row][current_col].append("up")
        if current_row == 0:
            return [current_row - 1, current_col]
        current_row -= 1
    current_row += 1
    return [current_row, current_col]

def travel_down(row, column):
    current_row = row
    current_col = column
    while not left_area(current_row, current_col) and input[current_row][current_col] != "#":    
        if "down" in visited[current_row][current_col]:
            return [current_row, current_col, "loop"]
        visited[current_row][current_col].append("down")
        if current_row == len(input) - 1:
            return [current_row + 1, current_col]
        current_row += 1
    current_row -= 1
    return [current_row, current_col]

def travel_left(row, column):
    current_row = row
    current_col = column
    while not left_area(current_row, current_col) and input[current_row][current_col] != "#":
        if "left" in visited[current_row][current_col]:
            return [current_row, current_col, "loop"]
        visited[current_row][current_col].append("left")
        if current_col == 0:
            return [current_row, current_col - 1]
        current_col -= 1
    current_col += 1
    return [current_row, current_col]


def travel(row, column, direction):
    new_starting = [-1, -1]
    if direction == "up":
        new_starting = travel_up(row, column)
    if direction == "right":
        new_starting = travel_right(row, column)
    if direction == "left":
        new_starting = travel_left(row, column)
    if direction == "down":
        new_starting = travel_down(row, column)
    new_direction = next_direction[direction]
    new_starting.append(new_direction)
    return new_starting

answer = 0
current_row = start_row
current_col = start_col
current_direction = "up"
while not left_area(current_row, current_col):
    #print(f"{current_row} {current_col} going direction {current_direction}")
    result = travel(current_row, current_col, current_direction)
    current_row = result[0]
    current_col = result[1]
    current_direction = result[2]

for list in visited:
    for item in list:
        if len(item) > 0:
            answer += 1
print(answer)


num_loops = 0
for i in range(len(input)):
    for j in range(len(input[0])):
        if input[i][j] == ".":
            for line in visited:
                for list in line:
                    list.clear()
            input[i] = input[i][:j] + "#" + input[i][j + 1:]
            #check if this causes a loop
            current_row_2 = start_row
            current_col_2 = start_col
            dir = "up"
            is_loop = False
            while not left_area(current_row_2, current_col_2) and not is_loop:
                result = travel(current_row_2, current_col_2, dir)
                if result[2] == "loop":
                    is_loop = True
                    num_loops += 1
                else:
                    current_row_2 = result[0]
                    current_col_2 = result[1]
                    dir = result[2]
            input[i] = input[i][:j] + "." + input[i][j + 1:]



print(num_loops)