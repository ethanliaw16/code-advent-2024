import sys
import time

#files keys are ID's
#vals are lists of blocks for the respective file id
#input 234 -> 00...1111 -> files are:
#(0) -> [0, 1]
#(1) -> [5,6,7,8]
files = {}

#list of blocks not currently used
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

def insert_in_order(new_elem, list):
    #print(f"insert {new_elem} into {list}")
    inserted = False
    for elem in list:
        if new_elem < elem:
            inserted = True
            list.insert(list.index(elem), new_elem)
            return list
    if not inserted:
        list.append(new_elem)
    return list

def highest_file_index():
    current_max = 0
    for file in files:
        current_max = max(current_max, max(files[file]))
    return current_max

def line_without_newline(line):
    return line[:-1]

def checksum(files):
    answer = 0
    for key in files:
        for item in files[key]:
            answer += key * item
    return answer

def is_contiguous(lst):
    # Check if the list has fewer than two elements (cannot check difference)
    if len(lst) < 2:
        return True

    # Iterate through the list and check the difference between consecutive elements
    for i in range(1, len(lst)):
        if lst[i] != lst[i - 1] + 1:
            return False

    return True    

#check for the presence of a contiguous set of block indices of length <size> 
#whose highest index is less than (to the left of) <end>, starting at the left-most (assume <spaces> is sorted)
#return [true, [<existing contiguous blocks>]] if found otherwise [False, empty]
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

#Pasting in terminal cuts off input, so had to read from a file.
with open('day-9-input.txt', 'r') as file:
    start_time = time.time()
    # Read the entire contents of the file as a string
    input_str = file.read()
    #input_str = "2333133121414131402n"
    handle(line_without_newline(input_str))

    
    current_rightmost_id = max(files.keys())
    free_spaces.sort()

    #Continue until all the spaces are contiguous on the right-hand side of the disc
    #i.e. the left most  free space is right of the right-most file block. 
    while(free_spaces[0] < highest_file_index()):
        right_most_file = files[current_rightmost_id]
        new_file = []
    
        #The instructions indicated that the right most file's blocks should get moved
        #starting from right to left. This approach went left-to-right. However, 
        #the result is the same: 
        #case 1: there was enough free space to the left of the file that every block 
        #of the file got moved -> same spaces are occupied and un-occupied in both cases.
        #case 2: there was only enough left-hand space for part of the file. Then, 
        #The remainder of the file will move to the free space that is created when the left-hand blocks
        #of the file when they were moved to free space. 
        for block in right_most_file:
            next_space = free_spaces[0]
            if next_space < block:
                new_file.append(free_spaces.pop(0))
                if block not in free_spaces:
                    #For some reason that is currently beyond me, it is faster to do this 
                    #than to insert the free space in the correct in-order position. 
                    #most likely to do with my laziness. 
                    free_spaces.append(block)
                    free_spaces.sort()
            else:
                new_file.append(block)
    
        files[current_rightmost_id] = new_file
        current_rightmost_id -= 1
        #I haven't been able to confirm this, but it appears that because the maximum possible 
        #contiguous free space to the left of a file must be 9 or less, all free spaces will be 
        # moved to the far right-hand side before all files have been (un)de-fragged. 
        #otherwise this would not work. 
    answer = checksum(files)
    print(f"part 1 {answer}")
    day_1_time = time.time()
    day_1_execution_time = day_1_time - start_time
    print(f"Execution time: {day_1_execution_time:.6f} seconds")


    #----------------Part 2----------------
    files = {}
    free_spaces = []
    handle(line_without_newline(input_str))
    current_rightmost_id = max(files.keys())
    free_spaces.sort()

    #Essentially the same as 1, but with a check that a big enough contiguous gap exists
    #before the move.
    while(current_rightmost_id >= 0):
        right_most_file = files[current_rightmost_id]
        right_file_size = len(right_most_file)
        check_for_left_space = enough_space_left(right_most_file[0], right_file_size, free_spaces)
        if check_for_left_space[0]:
            target_blocks = check_for_left_space[1]
            for block in target_blocks:
                free_spaces.remove(block)
            new_file = []
            for block in right_most_file:
                new_file.append(target_blocks.pop(0))
                free_spaces.append(max(free_spaces) + 1)
            files[current_rightmost_id] = new_file
        current_rightmost_id -= 1
    
    answer = checksum(files)
    print(f"part 2 {answer}")
    end_time = time.time()
    execution_time = end_time - day_1_time
    print(f"Execution time: {execution_time:.6f} seconds")
        





