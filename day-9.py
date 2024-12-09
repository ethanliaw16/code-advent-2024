import sys

input = {}
files = {}
free_spaces = []

def handle(line):
    if line != "":
        id = 0
        pos = 0
        for i in range(len(line)):
            current_char = int(line[i])
            if i%2 == 0:
                #file takes up <current_char> spaces 
                file_entry = []
                for j in range(current_char):
                    file_entry.append(j + pos)
                files[id] = file_entry
                id += 1
            else:
                for j in range(current_char):
                    free_spaces.append(pos + j)
            pos += current_char
        print(f"last pos is {pos} highest id is {max(files.keys())}")
        #print(files)
        #print(free_spaces)

lastline='a'

def highest_file_index():
    current_max = 0
    for file in files:
        current_max = max(current_max, max(files[file]))
    return current_max

def line_without_newline(line):
    return line[:-1]

def reverse_files(files):
    rev_files = {}
    for key in files:
        for item in files[key]:
            rev_files[item] = key
    return rev_files

def is_contiguous(lst):
    # Check if the list has fewer than two elements (cannot check difference)
    if len(lst) < 2:
        return True

    # Iterate through the list and check the difference between consecutive elements
    for i in range(1, len(lst)):
        if lst[i] != lst[i - 1] + 1:
            return False

    return True    


def enough_space_left(end, size, spaces):
    current = 0
    while current < len(spaces) - 1 and spaces[current] < end:
        if current + size > len(spaces) - 1:
            return [False, []]
        subset = spaces[current:current + size]
        if is_contiguous(subset):
            return [True, subset]
        current += 1

    return [False, []]


with open('day-9-input.txt', 'r') as file:
    # Read the entire contents of the file as a string
    input_str = file.read()
    #input_str = "2333133121414131402n"
    handle(line_without_newline(input_str))
    current_rightmost_id = max(files.keys())
    free_spaces.sort()
    while(free_spaces[0] < highest_file_index()) and current_rightmost_id >= 0:
        right_most_file = files[current_rightmost_id]
        new_file = []
        for block in right_most_file:
            next_space = free_spaces[0]
            if next_space < block:
                new_file.append(free_spaces.pop(0))
                free_spaces.sort()
                if block not in free_spaces:
                    free_spaces.append(block)
            else:
                new_file.append(block)
        
        files[current_rightmost_id] = new_file
        current_rightmost_id -= 1
    rev_files = reverse_files(files)
    block_indices = [n for n in rev_files.keys()]
    block_indices.sort()
    answer = 0
    compressed = ""
    for i in block_indices:
        answer += i * rev_files[i]
        #print(f"{i}\t{rev_files[i]}")
        #compressed += str(rev_files[i])
    print(f"part 1 {answer}")

    #----------------Part 2----------------
    files = {}
    free_spaces = []
    handle(line_without_newline(input_str))
    current_rightmost_id = max(files.keys())
    free_spaces.sort()

    while(current_rightmost_id >= 0):
        #print(f"rightmost {current_rightmost_id}")
        right_most_file = files[current_rightmost_id]
        right_file_size = len(right_most_file)
        check_for_left_space = enough_space_left(right_most_file[0], right_file_size, free_spaces)
        if check_for_left_space[0]:
            target_blocks = check_for_left_space[1]
            #print(f"{current_rightmost_id} can be moved to {target_blocks}")
            for block in target_blocks:
                free_spaces.remove(block)
            new_file = []
            for block in right_most_file:
                new_file.append(target_blocks.pop(0))
                free_spaces.append(max(free_spaces) + 1)
            files[current_rightmost_id] = new_file
        current_rightmost_id -= 1
    
    rev_files = reverse_files(files)
    #print(files)
    #print(free_spaces)
    block_indices = [n for n in rev_files.keys()]
    block_indices.sort()
    answer = 0
    for i in block_indices:
        answer += i * rev_files[i]
        #print(f"{i} {rev_files[i]}")
        
    print(f"part 2 {answer}")
        





