import sys


left = []
right = []
input = []
nonlist_input = []
def handle(line):
    if(line == ""):
        return 0
    input.append(line)
    nonlist_input.append(line)
    return 1

def without_nth_item(n, lst):
    return lst[:n] + lst[n+1:]

def line_without_newline(line):
    return line[:-1]

def num_xmas(row, column, board, height, width):
    num_found = 0
    #print(f"column {column} row {row}")
    if board[row][column] != "X":
        return num_found
    #to right
    if column + 4 <= width:
        
        if board[row][column:column + 4] == "XMAS":
            print(f"check right {board[row][column:column + 4]}")
            num_found += 1
        if row + 4 <= height:
            bottom_right = [board[row][column],
                             board[row + 1][column + 1], 
                             board[row + 2][column + 2], 
                             board[row + 3][column + 3]]
            
            if bottom_right == ["X","M","A","S"]:
                print(f"check bottom right {bottom_right}")
                num_found += 1
            
        if row - 3 >= 0:
            top_right = [board[row][column],
                             board[row - 1][column + 1], 
                             board[row - 2][column + 2], 
                             board[row - 3][column + 3]]
            
            if top_right == ["X","M","A","S"]:
                print(f"check top right {top_right}")
                num_found += 1

    #to_left
    if column - 3 >= 0:
        
        if board[row][column-3:column + 1] == "SAMX":
            print(f"check left {board[row][column-3:column + 1]}")
            num_found += 1
        if row + 4 <= height:
            bottom_left = [board[row + 3][column - 3],
                             board[row + 2][column - 2], 
                             board[row + 1][column - 1], 
                             board[row][column]]
            
            if bottom_left == ["S","A","M","X"]:
                print(f"check bottom left {bottom_left}")
                num_found += 1
        if row - 3 >= 0:
            top_left = [board[row - 3][column - 3],
                             board[row - 2][column - 2], 
                             board[row - 1][column - 1], 
                             board[row][column]]
            
            if top_left == ["S","A","M","X"]:
                print(f"check top left {top_left}")
                num_found += 1
    #down
    if row + 4 <= height:
        
        if [r[column] for r in board][row:row + 4] == ["X","M","A","S"]:
            print(f"check down {[r[column] for r in board][row:row + 4]}")
            num_found += 1
    #up
    if row - 3 >= 0:
        
        if [r[column] for r in board][row - 3:row + 1] == ["S","A","M","X"]:
            print(f'check up {[r[column] for r in board][row - 3:row + 1]}')
            num_found += 1
    return num_found

def is_x_mas(row, column, board, height, width):
    
    if(board[row][column] != "A"):
        return 0
    diag_1 = [board[row - 1][column - 1], board[row][column], board[row + 1][column + 1]]
    if diag_1 != ["M","A","S"] and diag_1 != ["S","A","M"]:
        return 0
    diag_2 = [board[row + 1][column - 1], board[row][column], board[row - 1][column + 1]]
    if diag_2 != ["M","A","S"] and diag_2 != ["S","A","M"]:
        return 0
    return 1

sum = 0
lastline='a'
for line in sys.stdin:
    if(line[:-1] == '' and lastline == ''):
        print("should be ending stdin")
        break
    else:
        sum += handle(line_without_newline(line))
        lastline = line[:-1]

i = 0

distances = 0

width = len(input[0])
height = len(input)

print(f"w {width} l {height}")
for y in range(len(input)):
    for x in range(len(input[0])):
        i += num_xmas(y, x, input, height, width)

print(f"{i} xmas total day 1")
i = 0
for y in range(len(input) - 2):
    for x in range(len(input) - 2):
        actual_y = y + 1
        actual_x = x + 1
        i += is_x_mas(actual_y, actual_x, input, height, width)
print(f"{i} xmas total")
    