import sys


left = []
right = []
input = []

def handle(line):
    if(line == ""):
        return 0
    input.append(line)
    return 1

def get_instruction(position, str):
    if(position + 4 > len(str)):
        return [0, 0]
    if(position + 7 > len(str)):
        return [0,0]
    dont_prefix = str[position:position + 7]
    if(dont_prefix == "don't()"):
        return [0,0,-1]
    do_prefix = str[position:position + 4]
    if(do_prefix == "do()"):
        return [0,0,1]
    instr_prefix = str[position:position + 4]
    if(instr_prefix != "mul("):
        return [0, 0]
    first_num_digit = position + 4
    
    if(not str[first_num_digit].isdigit()):
        return [0, 0]
    first_num_digit += 1
    end_num = not str[first_num_digit].isdigit()
    big_num = False
    while(first_num_digit <= position + 6 and not end_num):
        if not str[first_num_digit].isdigit():
            end_num = True
        else:
            first_num_digit += 1
            big_num = True
    first_num = int(str[position + 4])
    if(big_num):
        first_num = int(str[position + 4:first_num_digit])
    if(str[first_num_digit] != ","):
        return [0, 0]
    
    second_num_digit = first_num_digit + 1
    if(not str[second_num_digit].isdigit()):
        return [0, 0]
    second_num_digit += 1
    end_num_2 = not str[second_num_digit].isdigit()
    big_num_2 = False
    while(second_num_digit < first_num_digit + 5 and not end_num_2):
        if not str[second_num_digit].isdigit():
            end_num_2 = True
        else:
            second_num_digit += 1
            big_num_2 = True
    second_num = int(str[first_num_digit + 1])
    if big_num_2:
        second_num = int(str[first_num_digit + 1:second_num_digit])
    if(str[second_num_digit] != ")"):
        return [0, 0]
    print(f"{position} to {second_num_digit + 1} {str[position:second_num_digit + 1]} -> {first_num} x {second_num}")
    return [first_num, second_num]

def without_nth_item(n, lst):
    return lst[:n] + lst[n+1:]

def line_without_newline(line):
    return line[:-1]

input = ""

lastline='a'
for line in sys.stdin:
    if(line[:-1] == '' and lastline == ''):
        print("should be ending stdin")
        break
    else:
        input += (line_without_newline(line))
        lastline = line[:-1]


with open('day-3-input.txt', 'r') as file:
    # Read the entire contents of the file as a string
    input = file.read()
    small_input = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    #input = small_input
    enabled = True
    result = 0
    print("doing loop")
    for i in range(len(input) - 8):
        instr = get_instruction(i, input)
        if(enabled):
            result += instr[0] * instr[1]
        if(len(instr) > 2):
            if instr[2] == -1:
                enabled = False
            else:
                enabled = True

    print(f"input length {len(input)}")
    print(result)
    